# EBK Admin — Käyttöohje

Tämä ohje auttaa sinua hallinnoimaan Espoon Biljardikerhon verkkosivuja: lisäämään uutisia, tapahtumia ja jäseniä.

---

## 1. GitHub-tunnukset ja access token

Ennen kuin voit käyttää admin-työkalua, tarvitset GitHub-tunnukset ja **henkilökohtaisen access tokenin**. Token on kuin pitkä salasana, jolla työkalu voi tallentaa muutokset puolestasi GitHubiin.

### 1.1 Luo GitHub-tunnus (jos sinulla ei vielä ole)

1. Mene osoitteeseen https://github.com/signup
2. Anna sähköposti, salasana ja käyttäjänimi
3. Vahvista sähköposti
4. Pyydä ylläpitäjältä lisäys EBK:n repositorioon (`espoonbiljardikerho/sivut`)

### 1.2 Luo access token

1. Kirjaudu GitHubiin
2. Klikkaa profiilikuvaa oikeassa yläkulmassa → **Settings**
3. Vasemmalla alhaalla: **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**
6. Täytä:
   - **Note:** "EBK admin" (vapaa kuvaus)
   - **Expiration:** 90 päivää tai pidempi (huom: token vanhenee, joudut luomaan uuden)
   - **Scopes:** rastita ainoastaan **repo** (kaikki repo-alavalinnat valikoituvat automaattisesti)
7. Klikkaa **Generate token** sivun alalaidassa
8. **TÄRKEÄÄ:** Kopioi token heti talteen (esim. salasanahallintaan). Token näkyy vain kerran!
   - Token alkaa kirjaimilla `ghp_` ja on noin 40 merkkiä pitkä

> ⚠️ **Älä jaa tokenia kenellekään.** Se antaa täydet oikeudet repositorioon. Jos token vuotaa, käy poistamassa se GitHubin asetuksista heti.

---

## 2. Admin-sivun löytäminen

Admin-työkalu on osoitteessa:

**https://espoonbiljardikerho.fi/admin.html**

(Korvaa "espoonbiljardikerho.fi" oikealla domainilla, jos osoite eroaa.)

Suosittelemme tallentamaan sivun kirjanmerkkeihin.

---

## 3. Sisäänkirjautuminen

1. Avaa admin-sivu yllä olevasta osoitteesta
2. Anna kaksi tietoa:
   - **Salasana:** kerhon yhteinen admin-salasana (kysy ylläpitäjältä)
   - **GitHub Token:** kohdassa 1.2 luomasi token (`ghp_...`)
3. Klikkaa **Kirjaudu sisään**

Token tallentuu vain omaan selaimeesi — sitä ei lähetetä mihinkään palvelimelle. Tämä tarkoittaa että:
- Sinun ei tarvitse antaa tokenia uudelleen samalla koneella ja selaimella
- Jos vaihdat konetta tai selainta, joudut antamaan tokenin uudelleen
- Voit kirjautua ulos painikkeella (poistaa tokenin selaimesta)

---

## 4. Toiminnot

### 4.1 Jäsenten lisääminen

1. Vasemmasta valikosta **Jäsenet**
2. Oikealla yläkulmassa **+ Uusi jäsen**

Täytä lomake:

| Kenttä | Selitys |
|---|---|
| **Nimi** *(pakollinen)* | Etunimi Sukunimi |
| **Lempinimi** | Näkyy nimen perässä lainausmerkeissä |
| **Tyyppi** | Jäsenyyden taso (selitykset alla) |
| **Lajit** | Pilkulla erotellut: `Kaisa, Pool, Snooker` |
| **Liittynyt** | Vapaa tekstikenttä, esim. "2018" |
| **Aloittanut pelaamaan** | Vapaa tekstikenttä |
| **Motto / Lause** | Lyhyt sitaatti |
| **Bio** | Vapaa kuvausteksti |
| **Kuva** | Profiilikuva (katso 4.4) |

**Jäsentyypit:**
- **Täysjäsen** — kerhon varsinainen jäsen, äänioikeus
- **Klubijäsen** — kerhon jäsen ilman äänioikeutta
- **Pelaajajäsen** — pelaa kerhossa, ei vakituinen jäsen

> ⚠️ **Jos kahdella jäsenellä on sama nimi**, työkalu antaa virheilmoituksen ("Slug on jo käytössä"). Lisää tällöin lempinimi tai erotin nimeen, esim. "Matti Meikäläinen Jr".

### 4.2 Tapahtumien lisääminen

1. Vasemmasta valikosta **Tapahtumat**
2. Oikealla yläkulmassa **+ Uusi tapahtuma**

Tärkeimmät kentät:

| Kenttä | Selitys |
|---|---|
| **Nimi** *(pakollinen)* | Tapahtuman näkyvä nimi |
| **Laji** | Pelilaji (Kaisa/Pool/Snooker/Kara/Pyramidi) |
| **Alkamisaika** | Tekstikenttä, esim. "18:00" |
| **Alkaa** *(pakollinen)* | Tapahtuman päivämäärä |
| **Päättyy** | Jätä tyhjäksi yksittäiselle päivälle. Sarjatapahtumalle anna päättymispäivä |
| **Osallistumismaksu** | Esim. "30 €" tai "ilmainen" |
| **Ilmoittautuminen mennessä** | Esim. "Pe 14.8. klo 12:00 mennessä" |
| **Pelipaikka** | Oletuksena "Espoon Biljardi Klubi" |
| **Kenelle** | Kenelle tapahtuma on tarkoitettu (selitykset alla) |
| **Tila** | Tuleva / Mennyt — vaihda manuaalisesti tapahtuman jälkeen |
| **Paikkamäärä** | "käytetty/max" — esim. 5/16 = 5 ilmoittautunutta, max 16 paikkaa |
| **Järjestäjä** | Nimi ja sähköposti yhteyshenkilölle |
| **Aikataulu** | Vapaa tekstialue, yksi rivi per kohta: `09:00 Aloitus` |
| **Kuvaus** | Pidempi kuvaus tapahtumasta |

**"Kenelle" -vaihtoehdot:**
- **Jäsenille** — vain kerhon jäsenille (oletus)
- **Avoin kaikille** — kuka tahansa voi osallistua
- **Kutsuvierasturnaus** — vain kutsutut

> 💡 **Vinkki:** Kun tapahtuma on ohi, muista vaihtaa **Tila → Mennyt**. Muuten se näkyy edelleen "tulevien" listalla.

> ⚠️ **Käytetty-paikkamäärää** ei voi asettaa suuremmaksi kuin maksimi. Työkalu leikkaa sen automaattisesti.

### 4.3 Uutisten lisääminen

1. Vasemmasta valikosta **Uutiset**
2. Oikealla yläkulmassa **+ Uusi uutinen**

| Kenttä | Selitys |
|---|---|
| **Otsikko** *(pakollinen)* | Uutisen otsikko |
| **Slug** | URL-tunniste (luodaan automaattisesti otsikosta — älä yleensä muuta) |
| **Päivämäärä** *(pakollinen)* | Uutisen julkaisupäivä |
| **Laji** | Uutinen / Kaisa / Pool / Snooker / Kara / Pyramidi |
| **Kuva** | Pääkuva (katso 4.4) |
| **Lyhyt kuvaus** | Näkyy listoilla otsikon alla — pidä alle 150 merkkiä |
| **Sisältö** | Varsinainen artikkelin teksti, RTF-editorilla |

**Tekstieditori (Sisältö-kenttä):**

Yläpalkin painikkeet:
- **B** — lihavointi
- **I** — kursiivi
- **≡** — luettelo (lista)
- **🔗** — linkki: maalaa teksti ensin, sitten klikkaa, anna URL
- **Tyhjennä** — poistaa muotoilun valitusta tekstistä

**Kuvien lisääminen sisältöön:**
- Kopioi-liitä kuva suoraan editoriin (Ctrl+V) — kuva latautuu ja korvautuu automaattisesti

> ⚠️ **Mitä EI saa tehdä:**
> - Älä kopioi-liitä koko verkkosivua tai pitkiä HTML-pätkiä — editori ei välttämättä siivoa muotoilua kunnolla
> - Älä lisää erittäin suuria kuvia (yli 8 MB) — työkalu hylkää ne
> - Älä käytä videoita tai äänitiedostoja — vain tekstiä, kuvia ja linkkejä

### 4.4 Kuvien lisääminen (yhteinen ohje)

Kuvia voi lisätä uutisille, tapahtumille ja jäsenille.

**Kuvan lisäystavat:**
1. **Lataa tiedostosta** — klikkaa "📷 Klikkaa ladataksesi kuva" -aluetta, valitse tiedosto
2. **Käytä olemassa olevaa repokuvaa** — klikkaa "📁 Repo" -painiketta, valitse aiemmin ladattu kuva

**Tekniset rajat:**
- **Maksimikoko:** 8 MB (työkalu hylkää suuremmat)
- **Sallitut formaatit:** JPG, PNG, WebP
- **Automaattinen pakkaus:** työkalu pienentää kuvan automaattisesti enintään 900 pikseliin leveälle/korkealle ja pakkaa sen JPEG-muotoon (laatu 75 %). Et siis menetä mitään, jos lataat ison kuvan.

**Hyviä kuvanottokäytäntöjä:**
- Käytä vaakakuvia (1600 × 900 px on hyvä lähtökoko)
- Vältä kuvia, joissa on tärkeää tekstiä — tekstistä tulee epäselvä pakkauksen jälkeen
- Tallenna originaali alkuperäisellä laadulla erikseen — pakattua versiota ei voi palauttaa

---

## 5. Synkronointi ja tallentaminen

### 5.1 Miten tallentaminen toimii

EBK-sivut toimivat ilman erillistä tietokantaa. Kaikki tieto on **JSON-tiedostoissa** GitHubissa:
- `data/uutiset.json` — uutiset
- `data/tapahtumat.json` — tapahtumat
- `data/jasenet.json` — jäsenet
- `data/uutiset-archive.json` — vanhemmat uutiset (luodaan vain tarvittaessa)

Kun tallennat muutoksen admin-työkalussa:
1. Työkalu lähettää muutoksen suoraan GitHubiin (käyttäen tokeniasi)
2. GitHub tallentaa muutoksen committina
3. Verkkosivut päivittyvät **noin 30 sekunnissa** automaattisesti

> 💡 Älä huoli, jos sivut eivät näy heti päivittyneenä — odota minuutti ja päivitä selain.

### 5.2 Tallennuksen seuraaminen

Tallennuksen aikana:
- **Kultainen palkki** sivun yläreunassa kertoo mitä työkalu tekee ("Tallennetaan…")
- **Sivupalkki harmaantuu** estääkseen päällekkäiset toiminnot
- Lopuksi näkyy vihreä **"Tallennettu ✓"** -ilmoitus oikeassa alakulmassa

### 5.3 Synkronointi-sivu

**Synkronointi (↻)** -sivulla voit:
- **Tarkistaa tilan** — varmistat että GitHubissa olevat tiedostot ovat saatavilla
- Nähdä **kuinka monta** uutista, tapahtumaa ja jäsentä järjestelmässä on
- (Vain ylläpitäjille:) **Ylläpito**-osio sisältää vanhojen uutisten arkistoinnin — älä koske, ellet tiedä mitä teet

### 5.4 Virheiden käsittely

Jos jotain menee pieleen, sivun yläosaan ilmestyy **punainen virhepalkki**:

- **Lue viesti rauhallisesti** — useimmat virheet ovat helposti ratkaistavia
- Klikkaa **"Näytä lisätiedot"** nähdäksesi tekniset tiedot
- Klikkaa **"Kopioi"** kopioidaksesi virheilmoituksen leikepöydälle (kätevä, jos kysyt apua ylläpitäjältä)
- **"Sulje"** piilottaa palkin

**Yleisimmät virheet:**

| Virhe | Selitys |
|---|---|
| "Token vanhentunut tai virheellinen" | Token on vanhentunut. Luo uusi (kohta 1.2) ja kirjaudu uudelleen |
| "Verkkoyhteysongelma" | Internet-yhteys katkesi. Tarkista yhteys |
| "Yhtäaikainen muokkaus" | Joku toinen muokkasi samaa tiedostoa juuri. Lataa sivu uudelleen ja yritä uudelleen |
| "Slug on jo käytössä" | Antamasi nimi/otsikko tuottaa saman URL-tunnisteen kuin jokin olemassa oleva. Muuta nimeä |
| "GitHub-rajoitus saavutettu" | Liian monta tallennusta lyhyessä ajassa. Odota minuutti ja yritä uudelleen |

### 5.5 Yleisiä neuvoja

- **Yksi muokkaaja kerrallaan** — vältä että kaksi henkilöä muokkaa samaa asiaa samanaikaisesti
- **Älä sulje välilehteä tallennuksen aikana** — odota että kultainen palkki häviää
- **Päivämääräformaatti:** käytä päivämääräkenttiä, työkalu tallentaa muodossa "5.5.2026"
- **Jos epäilet jotain meneen pieleen** — älä yritä uudelleen heti. Tarkista GitHubista (data/-kansio) että tiedostot näyttävät oikealta. Kysy apua ylläpitäjältä.

---

## Apua ja yhteystiedot

Kysy apua kerhon ylläpitäjältä, jos:
- Et saa luotua tokenia
- Sivuston pääsy ei toimi
- Et ole varma jonkin toiminnon vaikutuksesta
- Saat virheilmoituksen, jota et ymmärrä

**Älä koskaan jaa GitHub-tokeniasi tai admin-salasanaa kenellekään.**
