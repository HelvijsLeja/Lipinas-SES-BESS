# Ļipiņas SES + BESS

Vienas lapas vizītkarte (teaser) saules elektrostacijas (SES) un akumulatoru
enerģijas uzkrāšanas (BESS) parka projektam **"Ļipiņas"**, Salaspils pagastā,
Salaspils novadā.

## Par projektu

- **SES:** 3 MWp saules paneļu jauda (2,5 MW tīklā)
- **BESS:** 5 MWh akumulatoru ietilpība (2,5 MW tīklā)
- **Zemes gabali:** "Ļipiņas" (kad. 8031 014 0020) un "Ļipiņas 1" (kad. 8031 014 0315)
- **Statuss:** tīkla pieslēgums SES vajadzībām nodots ekspluatācijā; notiek projekta
  papildināšana ar BESS

Attīstītājs: SIA "STROIPERLIT-RIGA".

## Tehniskais

Viens pašpietiekams `index.html` fails. Bez build soļa. Ārējās atkarības (no CDN):

- [Leaflet](https://leafletjs.com/) — karte
- [OpenStreetMap](https://www.openstreetmap.org/) / [OpenTopoMap](https://opentopomap.org/) — kartes slāņi
- Google Fonts (Space Grotesk, Inter)

Pieejamas 3 valodas (LV / EN / RU) ar pārslēgu; izvēle saglabājas pārlūkā.

### Kartes koordinātas

Zemesgabala atrašanās vieta konfigurējama `index.html` skripta augšā:

```js
const SITE_COORDS = [56.90378, 24.36294];
const SITE_ZOOM   = 14;
```

## Publicēšana (GitHub Pages)

Settings → Pages → Deploy from a branch → `main` / root. Lapa būs pieejama
`https://helvijsleja.github.io/Lipinas-SES-BESS/`.

---

_Skaitļi ir indikatīvi un nav publisks piedāvājums iegādāties vērtspapīrus._
