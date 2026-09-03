# Malibu Boats — NSW Primary Market Area

Interactive concept map for the New South Wales PMA supporting a new Malibu
dealership in Sydney.

![State overview](assets/state-overview.png)

> **New here?** Read [`HANDOVER.md`](HANDOVER.md) — full project state, decisions,
> open questions and limitations. [`NEW-SESSION-BRIEF.md`](NEW-SESSION-BRIEF.md)
> is a paste-ready brief for starting a fresh AI session on this project.

## The PMA rule

| Zone | Definition | Area |
|---|---|---|
| **Open Area 1** | Everything within **15 km north of the NSW/VIC border**, measured perpendicular to the border | 17,545 km² road-routed (17,670 km² geometric) |
| **Active PMA** | The balance of New South Wales + the ACT — the NSW dealer's area | 763,642 km² road-routed (763,497 km² geometric) |
| **Open Area 2** | The coastal strip from **Grafton north to the Queensland border**, held at Grafton's distance from the coast — **35.0 km**. The routed boundary runs west of Grafton so the whole city is inside, and its southern edge follows roads east to the sea at Diggers Camp | 6,526 km² road-routed (6,545 km² geometric) |

The Victorian border runs 1,753 km: the River Murray from the South Australian
corner up to its source, then the straight survey line south-east to Cape Howe.

Both open areas publish a **road-routed** boundary alongside the geometric line. The routed boundaries are the operative ones and are shown by default; the geometric lines stay available for comparison.

Every edge of both open areas is now routed. Open Area 2's southern edge — once a
straight line due east at 29.8073 S — follows Armidale Road, Braunstone Road, the
Orara Way, the Big River Way and the Pacific Highway, then Lookout, Stonehouse and
Wooli Roads to the sea at Diggers Camp: **65.1 km of boundary, 57.5 km of it on
roads**, in place of a 38.3 km line.

> **The whole of Grafton is inside Open Area 2.** The routed boundary runs west of
> the city, so Grafton, South Grafton, Junction Hill, Clarenza, Waterview Heights
> and Ulmarra all fall inside — on roads, with no separate ring-fence.
> Copmanhurst, Coutts Crossing, Casino and Kyogle stay outside.

## What's in the map

`index.html` is a single self-contained file — no build step, no server, no
dependencies. Open it in any browser.

- **State overview / Detail / Satellite** view modes
- Base mapping with roads, towns and labels drawn *above* the PMA shading
- Opacity slider to fade the overlays back
- Layer toggles for each zone, the border, and the 50 km line
- 4,118 towns and localities, each tagged with its zone and its distance from the Victorian border or from the coast
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

## Base mapping — vector, no API key

The map renders **vector tiles** with MapLibre GL JS:

| Mode | Style |
|---|---|
| State overview | OpenFreeMap **Positron** |
| Detail | OpenFreeMap **Liberty** |
| Satellite | Esri World Imagery (raster — imagery always is) |

[OpenFreeMap](https://openfreemap.org) is free, keyless and unmetered. Vector
means crisp labels and roads at every zoom, no `@2x` requests, and the PMA
fills are inserted **beneath the base map's own label layers** — so town and road
names always read on top of the shading, which the old raster build faked with a
second tile layer.

If the vector style can't be reached, the map falls back to Esri imagery and says
so on screen rather than showing a blank canvas.

Attribution is mandatory and appears bottom-right — leave it in place.
`scripts/verify_map.py` asserts every custom layer loads and reports which hosts
the page contacts (expected: `tiles.openfreemap.org`, `server.arcgisonline.com`).

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
data/pma.geojson            PMA polygons, border and boundary lines (WGS84)
data/towns.json             Localities with zone + distance to border
HANDOVER.md                 Project state, decisions, open questions, limitations
NEW-SESSION-BRIEF.md        Paste-ready context for a fresh session
docs/METHODOLOGY.md         How the geometry was computed, and its limits
data/oa2_route.txt          Open Area 2 — routed western boundary
data/oa2_south_route.txt    Open Area 2 — routed southern edge (Grafton area → coast)
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
| Road network — Open Area 1 | [Natural Earth 10m roads](https://www.naturalearthdata.com/) | Public domain |
| Road network — Open Area 2 (western edge) | OpenStreetMap via Overpass API | ODbL |
| Road network — Open Area 2 (southern edge) | OpenStreetMap via Overpass API | ODbL |
| Localities | [matthewproctor/australianpostcodes](https://github.com/matthewproctor/australianpostcodes) | Open |
| Base mapping | © OpenStreetMap contributors, © CARTO; imagery © Esri | ODbL / see providers |
| Map library | [MapLibre GL JS](https://maplibre.org/) 4.7.1 | BSD-3-Clause |

## Disclaimer

Concept map for PMA planning discussion. Boundaries are indicative and
this is not a legal instrument. Confirm any boundary against a surveyed
description before it goes into a dealer agreement.
