<?php
/**
 * Contact form handler for krscanskazajednicasibenik.hr.
 *
 * Only runs on the FTP hosting - the Vercel preview is static, so the form
 * there submits to nothing. Keep this file in the web root next to index.html.
 */
declare(strict_types=1);

const MAIL_TO   = 'info@krscanskazajednicasibenik.hr';
const MAIL_FROM = 'no-reply@krscanskazajednicasibenik.hr';

$lang = (isset($_POST['lang']) && $_POST['lang'] === 'en') ? 'en' : 'hr';
$home = $lang === 'en' ? '/en/' : '/';

/** Send the visitor back to the contact page with a status flag. */
function redirect_back(string $lang, string $status): void {
    $page = $lang === 'en' ? '/en/contact/' : '/kontakt/';
    header('Location: ' . $page . '?status=' . $status, true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . $home, true, 303);
    exit;
}

// Honeypot: a real visitor never sees this field, and no browser autofills a
// name like this one. Anything in it is a bot, so drop it silently.
if (trim((string)($_POST['hp_zz'] ?? '')) !== '') {
    redirect_back($lang, 'ok');
}

$name    = trim((string)($_POST['ime'] ?? ''));
$email   = trim((string)($_POST['email'] ?? ''));
$subject = trim((string)($_POST['tema'] ?? ''));
$message = trim((string)($_POST['poruka'] ?? ''));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    redirect_back($lang, 'error');
}

// Header injection guard: a newline in either field would let a sender append
// their own headers, so anything with one is rejected outright.
if (preg_match('/[\r\n]/', $name . $email . $subject)) {
    redirect_back($lang, 'error');
}

$name    = mb_substr($name, 0, 120);
$subject = mb_substr($subject, 0, 160);
$message = mb_substr($message, 0, 5000);

$mailSubject = 'Poruka sa stranice: ' . ($subject !== '' ? $subject : 'bez teme');
$body = "Ime: {$name}\n"
      . "E-mail: {$email}\n"
      . "Tema: " . ($subject !== '' ? $subject : '-') . "\n"
      . "Jezik: {$lang}\n"
      . "IP: " . ($_SERVER['REMOTE_ADDR'] ?? '-') . "\n"
      . "Vrijeme: " . date('Y-m-d H:i:s') . "\n\n"
      . "Poruka:\n{$message}\n";

$headers = [
    'From: Web obrazac <' . MAIL_FROM . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=UTF-8',
    'MIME-Version: 1.0',
];

$sent = @mail(
    MAIL_TO,
    '=?UTF-8?B?' . base64_encode($mailSubject) . '?=',
    $body,
    implode("\r\n", $headers)
);

redirect_back($lang, $sent ? 'ok' : 'error');
