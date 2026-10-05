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

`index.html` ir LV avots; `/en/`, `/de/`, `/ru/` ģenerē `python3 build.py` (rediģē tikai `index.html`, tad palaid skriptu). Leaflet un fonti ir vietnē (`leaflet/`, `fonts/`). Ārējās atkarības:

- [Leaflet](https://leafletjs.com/) 1.9.4 — karte (self-host)
- [OpenStreetMap](https://www.openstreetmap.org/) / [OpenTopoMap](https://opentopomap.org/) — kartes slāņi
- Fonti Space Grotesk, Inter — self-host

Četras valodas (LV / EN / DE / RU), katrai savs URL ar hreflang.

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
