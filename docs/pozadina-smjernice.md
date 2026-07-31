# Smjernice za novu pozadinu stranice

## Ukratko: pozadina ide prva, boje za njom

Sadašnja crno-bijela shema je radna verzija. Kad se odluči pozadina, iz nje
izvodimo logo, naglasak i sve ostalo. Zato za pozadinu vrijedi samo pet
pravila, a unutar njih je sve slobodno: tekstura, grafika, fotografija, bilo
koja boja.

1. **Prvo odlučite: svijetla ili tamna.** Ta jedna odluka povlači sve ostalo.
2. **Držite je na jednom kraju skale, ne u sredini.** Svijetlija od otprilike
   `#a0a0a0`, ili tamnija od otprilike `#595959`. Sredina je jedino što ne
   radi: na srednje sivoj podlozi ni tamni ni svijetli tekst nemaju dovoljno
   kontrasta. Na `#787878` tamni tekst daje 4.1:1, a bijeli 4.4:1, dakle oba
   padaju ispod minimuma od 4.5:1.
3. **Neka bude mirna.** Bez naglih skokova svijetlo/tamno na malom razmaku.
   Koliko je svijetla ili tamna podešavam ja, koliko je nemirna ne mogu.
4. **Malo zasićenja.** Pozadina je najveća površina na stranici. Jaka boja
   preko cijelog ekrana suzi sve ostale izbore. Boju stavite u naglasak, ne u
   pozadinu.
5. **Pošaljite uz nju jednu ili dvije boje izvučene iz same grafike.** Iz njih
   radim naglasak i boju logotipa, pa sve drži zajedno.

Iz toga slažem pet vrijednosti koje čine cijelu stranicu: pozadina, ploha
kartica, tekst, naglasak i tamna ploha za podnožje. Logo ide u jednoj punoj
boji koja se dovoljno odvaja od pozadine.

Ostatak dokumenta su tehnički detalji po formatima, za onoga tko crta.

---

Nova pozadina **u potpunosti zamjenjuje postojeću**. Ne dodaje se preko nje.

Još nije odlučeno hoće li to biti tekstura, grafika ili fotografija, pa su
ovdje sva tri smjera. Zajednička pravila (dio 3 i 4) vrijede za sve.

---

## 1. Što se točno mijenja

Sadašnja pozadina su dva sloja koja stoje fiksno i ne pomiču se pri skrolanju:

1. **Boja** - prijelaz iz `#f3f1ee` (vrh) preko `#e9e7e3` u `#dcd9d4` (dno)
2. **Tekstura** - vrlo sitan šum na 5% prozirnosti

Oba nestaju. Ono što pošaljete postaje **osnovni sloj cijele stranice**, na
svih 22 podstranice, na svakom uređaju.

**Gdje se pozadina zapravo vidi:** sadržaj stranice stoji na poluprozirnim
bijelim karticama i panelima (bijela na 66% prozirnosti). Pozadina se vidi u
razmacima između njih, uz rubove, te **djelomično kroz same kartice, ispod
teksta**. Nije to samo okvir oko sadržaja.

Tamni dijelovi (zaglavlje na naslovnoj, podnožje na svim stranicama) imaju
svoju pozadinu, pa se tamo vaša grafika ne vidi. Radi se samo jedna verzija.

---

## 2. Tri moguća smjera

### A. Tekstura (bešavni uzorak)

Najsigurniji izbor. Papir, platno, žbuka, zrno, fine linije.

- **Dimenzije:** 512 x 512 px ili 1024 x 1024 px, plus @2x verzija
- **Format:** PNG, ili SVG ako je geometrijski
- **Težina:** ispod 60 KB
- Mora biti **stvarno bešavan**. Provjera: pomaknite sadržaj za 50% vodoravno i
  okomito (Photoshop: Filter > Other > Offset). Ako se vidi linija spoja,
  nije gotovo.
- Može doći **prozirno**, pa boju i dalje držim u CSS-u i lako je mijenjam, ili
  **s upečenom bojom** ako uzorak i boja idu zajedno. Recite koje od toga.

### B. Grafika (ilustracija ili uzorak)

Crtani motiv, geometrija, apstraktni oblici.

- **Ako se ponavlja:** iste dimenzije kao pod A
- **Ako je jedna velika kompozicija:** najmanje 2560 x 1440 px, sigurnije
  3200 x 1800 px
- **Format:** SVG kad god je moguće, inače PNG ili WebP
- **Težina:** ispod 150 KB
- Motiv ne smije imati "gore" i "dolje" koje je bitno. Pozadina stoji fiksno
  dok sadržaj klizi preko nje, a stranice su različitih duljina.

### C. Fotografija

Najefektnije, ali traži najviše pažnje.

- **Dimenzije:** najmanje 2560 x 1440 px, poželjno 3200 x 1800 px
- **Uz to i okomita verzija za mobitel:** oko 1200 x 1800 px. Vodoravna
  fotografija na uskom visokom ekranu pokaže samo mali isječak sredine, pa
  kompozicija propadne.
- **Format:** pošaljite original (JPEG iz aparata je u redu), pretvaranje u
  WebP i smanjivanje radim ja
- **Težina nakon obrade:** ispod 250 KB za desktop, ispod 120 KB za mobitel
- **Bez glavnog motiva.** Nešto mirno i ujednačeno: nebo, more, kamen, zid,
  magla, izmaglica nad gradom. Lice ili prepoznatljiv prizor iza teksta smeta
  i čitanju i samoj fotografiji.

**Preporuka:** ako niste sigurni, tekstura ili vrlo mirna fotografija.
Nagurana grafika izgleda dobro na jednoj slici, a zamori nakon treće
podstranice.

---

## 3. Kontrast, i zašto je to ovdje glavno pitanje

Tekst na stranici je tamno siv (`#171614`) i sada je izmjeren na omjeru
kontrasta 7:1. Minimum je 4.5:1.

Dvije stvari koje treba znati:

**Zatamnjenje ili posvjetljenje radim ja u CSS-u.** Ne morate fotografiju
unaprijed blijediti ni tamniti. Pošaljite je normalnu, ja preko nje stavljam
sloj koji podešavam dok mjerenje ne prođe. Isto radim i na naslovnoj, gdje je
preko fotografije tamni sloj.

**Ali podloga ispod teksta mora biti mirna.** Sloj preko nje rješava koliko je
svijetla ili tamna, ne rješava koliko je nemirna. Ako pozadina na malom
razmaku skače sa svijetlog na tamno, tekst je na jednom mjestu čitljiv, a
dva centimetra dalje nije. To je gore od ravne boje.

Praktično pravilo: **što je pozadina nemirnija, to kartice moraju biti
neprozirnije.** Sada su na 66%. Uz nemirnu pozadinu moram ih dići prema 90%,
a tada se kroz njih ionako više ništa ne vidi. Bujna pozadina tako sama sebe
poništi. Mirnija pozadina se zapravo bolje vidi.

### Ako pozadina bude tamna

To nije samo zamjena slike. Cijela paleta se okreće: tekst, kartice, gumbi,
obrasci, sve prelazi na svijetlo na tamnom, na svih 22 podstranice. To je
izvediva ali znatno veća prepravka. Recite unaprijed ako idete u tom smjeru.

---

## 4. Zajednička pravila

- **Boje:** sive i neutralne pristaju uz postojeći mjedeni naglasak
  (`#8c7a52`). Hladne plavkaste sive se s njim tuku. Jake zasićene boje ne.
- **Bez teksta i logotipa.** Znak Š se već pojavljuje kao vodeni žig na svakoj
  sekciji, lijevo pa desno pa u sredini, i tukli bi se.
- **Bez upečenih prijelaza boje** u rasterskoj slici, rade vidljive pruge
  (banding). Prijelaze radim u CSS-u.
- **Ne JPEG za teksturu i grafiku.** Na niskim kontrastima JPEG radi vidljive
  kvadratiće. Za fotografiju je JPEG original u redu.
- **Provjerite na 375 px širine.** Uzorak koji je fin na velikom monitoru zna
  na mobitelu postati napadan.
- **Težina se plaća na svakoj stranici.** Pozadina se učita svakom posjetitelju,
  na svakoj podstranici. Zato gornji limiti.

---

## 5. Što mi predati

1. Datoteku prema odabranom smjeru (A, B ili C), s @2x ili mobilnom verzijom
   gdje piše da treba
2. Za teksturu: recite je li prozirna ili nosi boju
3. Izvornu datoteku (AI, PSD, Figma) ako postoji, za slučaj prepravke
4. Jednu sliku "kako zamišljate da izgleda" na cijelom ekranu, da znam jesam li
   pogodio jačinu

Nazivi: `bg.png` / `bg.svg` / `bg.jpg`, uz `bg@2x.png` ili `bg-mobile.jpg`.
Idu u `assets/img/`.

---

## 6. Kako ću to ugraditi

Zamjenjuje se jedan blok u `styles.css`. Za uzorak:

```css
body::before {
  background-image: url("/assets/img/bg.png");
  background-repeat: repeat;
  background-size: 512px 512px;
}
```

Za fotografiju ili veliku kompoziciju, uz sloj za podešavanje svjetline:

```css
body::before {
  background-image:
    linear-gradient(rgba(246,245,242,.72), rgba(246,245,242,.72)),
    url("/assets/img/bg.jpg");
  background-size: auto, cover;
  background-position: center;
}
```

Nakon ugradnje ponovno mjerim kontrast teksta na svim stranicama i javljam
brojku prije nego što kažem da je gotovo.

---

## 7. Provjera prije slanja

- [ ] Ako se ponavlja: pomak za 50% ne otkriva šav
- [ ] Podloga je mirna ispod teksta, bez naglih skokova svijetlo/tamno
- [ ] Nema teksta, slova ni logotipa
- [ ] Nema jakih zasićenih boja
- [ ] Za fotografiju: poslana i okomita verzija za mobitel
- [ ] Za fotografiju: nema glavnog motiva koji traži pažnju
- [ ] Izgleda mirno i na 375 px širine
- [ ] Ako je pozadina tamna: dogovoreno unaprijed, jer mijenja cijelu paletu
