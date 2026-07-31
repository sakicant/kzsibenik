# Smjernice za izradu pozadine stranice

Kratko: treba mi **bešavni uzorak (seamless tile), prozirni PNG ili SVG, vrlo
niskog kontrasta**. Boju i jačinu podešavam ja u CSS-u.

---

## 1. Kako pozadina sada radi

Pozadina nije obična slika iza sadržaja. Sastoji se od dva sloja koja stoje
fiksno (ne pomiču se pri skrolanju):

1. **Sloj boje** - blagi prijelaz iz svjetlije sive na vrhu u tamniju pri dnu:
   - `#f3f1ee` (vrh)
   - `#e9e7e3` (sredina)
   - `#dcd9d4` (dno)
2. **Sloj teksture** - vrlo sitan šum, jedva vidljiv, na 5% prozirnosti.

Vaš uzorak zamjenjuje **sloj 2**. Sloj boje ostaje u CSS-u, pa ga mogu mijenjati
bez diranja vaše grafike.

**Zašto je to važno:** kartice i paneli na stranici su poluprozirni (bijela na
66% prozirnosti). Sve što je u pozadini djelomično se probija kroz njih, ispod
teksta. Zato uzorak mora biti miran.

---

## 2. Format

| Format | Kada | Napomena |
|---|---|---|
| **SVG** | najbolje, ako je uzorak geometrijski | Sitan (par KB), oštar na svim ekranima, nema retina verzije |
| **PNG s prozirnošću** | ako je uzorak crtan ili teksturiran | Treba i @2x verzija |
| **WebP** | samo ako je uzorak fotografski (papir, platno, beton) | Šaljem li ja pretvaranje, pošaljite original |

**Ne JPEG.** Na ovako niskim kontrastima JPEG radi vidljive kvadratiće i pruge.

**Pošaljite s prozirnom pozadinom**, ne s upečenom bojom. Tako mogu podesiti i
boju i jačinu, i ista datoteka radi ako kasnije promijenimo paletu.

---

## 3. Dimenzije

### Bešavni uzorak (preporučeno)

- **512 x 512 px** ili **600 x 600 px** na 1x
- **1024 x 1024 px** ili **1200 x 1200 px** na 2x (za retina ekrane)
- Ako je SVG, dimenzija nije bitna, samo neka je uzorak definiran kao ploča koja
  se ponavlja

Uzorak mora biti **stvarno bešavan**. Provjera: pomaknite sadržaj za 50% po
horizontali i vertikali (u Photoshopu Filter > Other > Offset). Ako se vidi
šav ili linija spoja, nije gotovo.

### Ako radite jednu veliku sliku umjesto uzorka

- **najmanje 2560 x 1440 px**, sigurnije 3200 x 1800
- najviše **300 KB** kao WebP
- Napomena: ovo je slabija opcija. Slika se rasteže preko cijelog ekrana, na
  širokim monitorima gubi oštrinu, a na mobitelu se vidi samo dio.

---

## 4. Boje i kontrast (najvažniji dio)

Ovo je jedino mjesto gdje se lako pogriješi.

- **Raspon svjetline unutar uzorka: najviše 8%.** Konkretno, ako je najsvjetlija
  točka `#f4f2ef`, najtamnija ne smije biti tamnija od otprilike `#e0ded9`.
- **Nikakve čiste crne ni bijele točke.**
- **Zasićenost blizu nule.** Sive s toplim tonom pristaju uz postojeću paletu.
  Hladne plavkaste sive će se tući s mjedenim naglaskom (`#8c7a52`).
- Ako radite prozirni PNG: crtajte crnom na **8% do 15% prozirnosti**, ne jače.
  Radije mi pošaljite prejako pa ja stišam, nego preslabo.

**Zašto ovako strogo:** tekst na stranici je tamno siv (`#171614`) i mjeren je
na omjeru kontrasta 7:1 prema podlozi. Pozadina koja varira više od par posto
spušta taj omjer na dijelovima stranice i tekst postaje teže čitljiv na nekim
mjestima, a ne na drugima. To je gore nego ravna pozadina.

---

## 5. Gustoća i veličina motiva

Dva sigurna smjera:

- **Sitno i gusto** - zrno, tkanina, papir, fine linije. Motiv ispod 4 px.
  Doima se kao tekstura materijala, ne kao uzorak.
- **Veliko i vrlo blago** - široki oblici preko 400 px, na samom rubu vidljivosti.

**Izbjegavajte sredinu** - motive od otprilike 20 do 150 px. To je veličina koja
najviše smeta čitanju jer se natječe s recima teksta.

Provjerite kako izgleda na mobitelu. Uzorak koji je fin na 1440 px zna postati
napadan na 375 px.

---

## 6. Što izbjegavati

- Tekst, slova, logotip. Znak Š se već pojavljuje kao vodeni žig na svakoj
  sekciji (lijevo, desno, sredina, u krug), pa bi se tukli.
- Oštre ravne linije po rubu ploče, tamo nastaju šavovi.
- Prijelaze boje upečene u sliku, rade pruge (banding). Prijelaz radim u CSS-u.
- Prepoznatljive fotografije. Pozadina ide ispod svega, na svim stranicama.
- Uzorak koji se očito ponavlja. Ako se u pogledu na cijeli ekran broji koliko
  puta se nešto ponovilo, ploča je premala ili motiv prejak.

---

## 7. Što mi predati

1. Uzorak, prozirni PNG na 1x i 2x, ili SVG
2. Ako imate, izvornu datoteku (AI, PSD, Figma) za slučaj prepravke
3. Jednu sliku "kako bi trebalo izgledati" na cijelom ekranu, da znam jesam li
   dobro pogodio jačinu

Nazivi datoteka: `bg-tile.png`, `bg-tile@2x.png`, `bg-tile.svg`. Idu u
`assets/img/`.

---

## 8. Kako ću to ugraditi

Zamjena je jedan blok u `styles.css`:

```css
body::after {
  background-image: url("/assets/img/bg-tile.png");
  background-repeat: repeat;
  background-size: 512px 512px;   /* veličina ploče na 1x */
  opacity: .06;                    /* ovdje podešavam jačinu */
}
```

Jačinu i veličinu ploče podešavam nakon što vidim kako izgleda uživo, pa oko
toga ne morate brinuti. Također ću ponovno izmjeriti kontrast teksta na svim
stranicama prije nego što potvrdim da je gotovo.

---

## 9. Brza provjera prije slanja

- [ ] Pomak za 50% ne otkriva šav
- [ ] Razlika najsvjetlije i najtamnije točke ispod 8%
- [ ] Nema čiste crne ni bijele
- [ ] Nema teksta ni logotipa
- [ ] Prozirna pozadina, boja nije upečena
- [ ] PNG ili SVG, ne JPEG
- [ ] Izgleda mirno i na 375 px širine

---

## Napomena o tamnim dijelovima

Zaglavlje na naslovnoj i podnožje na svim stranicama su tamni i imaju svoju
pozadinu, pa se ovaj uzorak tamo ne vidi. Trebate raditi samo svijetlu verziju.
