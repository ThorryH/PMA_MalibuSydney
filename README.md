# Malibu Boats — NSW Primary Market Area

Interactive concept map for the New South Wales PMA supporting a new Malibu
dealership in Sydney.

![State overview](assets/state-overview.png)

## The territory rule

| Zone | Definition | Area |
|---|---|---|
| **Open Area 1** | Everything within **50 km north of the NSW/VIC border**, measured perpendicular to the border | 53,600 km² |
| **NSW dealer active territory** | The balance of New South Wales + the ACT | 734,100 km² |
| **Open Area 2** | Not yet defined | — |

The border itself runs 1,753 km: the River Murray from the South Australian
corner up to its source, then the straight survey line south-east to Cape Howe.

## What's in the map

`index.html` is a single self-contained file — no build step, no server, no
dependencies. Open it in any browser.

- **State overview / Detail / Satellite** view modes
- Base mapping with roads, towns and labels drawn *above* the territory shading
- Opacity slider to fade the overlays back
- Layer toggles for each zone, the border, and the 50 km line
- 3,331 towns and localities, each tagged with its zone and distance from the border
- **Point check** — click anywhere to get the zone, the exact distance to the border, and the nearest locality
- Town search

### Password

`index.html` is password-protected. The map is encrypted with AES-256-GCM
inside the file; the key is derived from the password with PBKDF2-HMAC-SHA256
(250,000 iterations). Viewing source shows ciphertext only. Decryption happens
entirely in the browser — nothing is transmitted, and it works offline.

Default password: **`malsyd`**

To change it, rebuild with `make lock PW=newpassword`.

> **Note:** anyone with the password can save the decrypted page. Treat this as
> controlling distribution, not as a guarantee against a determined leak.

## Publishing to GitHub Pages

1. Push this repository to GitHub.
2. **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The map is live at `https://<user>.github.io/<repo>/`.

`.nojekyll` is included so Pages serves the files as-is.

> `local/` holds the **unprotected** copy of the map and is git-ignored. Keep it
> that way — committing it would defeat the password.

## Repository layout

```
index.html                  Password-protected map (this is what gets published)
assets/state-overview.png   Static state-level overview
data/pma.geojson            Territory polygons, border and boundary lines (WGS84)
data/towns.json             Localities with zone + distance to border
docs/METHODOLOGY.md         How the geometry was computed, and its limits
scripts/                    Reproducible build
local/                      Unprotected map — git-ignored
```

## Rebuilding

```bash
pip install -r scripts/requirements.txt
make            # fetch data → compute geometry → build map → apply password
```

Individual steps: `make data`, `make geometry`, `make map`, `make lock PW=…`.

## Data sources

| Dataset | Source | Licence |
|---|---|---|
| State boundaries | [rowanhogan/australian-states](https://github.com/rowanhogan/australian-states) | Open |
| Road network | [Natural Earth 10m roads](https://www.naturalearthdata.com/) | Public domain |
| Localities | [matthewproctor/australianpostcodes](https://github.com/matthewproctor/australianpostcodes) | Open |
| Base mapping | © OpenStreetMap contributors, © CARTO; imagery © Esri | ODbL / see providers |
| Map library | [Leaflet](https://leafletjs.com/) 1.9.4 | BSD-2-Clause |

## Disclaimer

Concept map for territory planning discussion. Boundaries are indicative and
this is not a legal instrument. Confirm any boundary against a surveyed
description before it goes into a dealer agreement.
