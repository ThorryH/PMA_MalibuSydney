# Malibu Boats — NSW PMA · Project Handover

Everything needed to pick this up cold. Written for whoever works on it next,
including a fresh AI session with no memory of how it was built.

---

## 1. What this project is

A Primary Market Area (PMA) concept map for **New South Wales**, drawn to support
a **new Malibu Boats dealership in Sydney**.

The PMA is the whole of NSW + the ACT, minus two carve-outs called **Open Areas**
where no dealer holds the area. Everything else is the **Active PMA**, held by the
NSW dealer.

There is no third open area. Nothing is committed contractually — this is a
planning artefact, not a legal instrument.

## 2. The rules as currently built

| Area | Rule | Road-routed | Geometric |
|---|---|---|---|
| **Open Area 1** | Within **15 km north of the NSW/VIC border**, measured perpendicular to the border, plus **Deniliquin** behind a 5 km road-routed boundary | **17,993 km²** | 18,060 km² |
| **Open Area 2** | Coastal strip from **Grafton north to the Queensland border**, held at Grafton's own distance from the coast (**35.0 km**), plus **Casino** behind a 5 km road-routed boundary; southern edge routed on roads east to the sea at Diggers Camp | **6,754 km²** | 6,706 km² |
| **Active PMA** | The balance of NSW + ACT, held 500 m clear of the QLD border | **762,558 km²** | 762,539 km² |

The NSW/VIC border itself measures **1,753 km** — the River Murray from the South
Australian corner to its source, then the straight survey line to Cape Howe. The
NSW/QLD border measures **1,681 km** over 4,845 vertices, from OpenStreetMap's
administrative boundary; the two borders are at different resolutions, because
only Queensland was in scope for the setback work.

Two boundary versions exist for each open area. The **road-routed** version is the
operative one and is shown by default. The **geometric** version is the pure
distance line, kept for comparison and as the definition of record.

### Rule history — how it got here

1. Open Area 1 was originally **50 km** (53,600 km²), reduced to **15 km**, then
   extended to take in **Deniliquin** behind its own 5 km road-routed boundary.
2. Open Area 2's southern edge was originally a line through Grafton. It moved
   south to **29.8073 S** so the whole city sits inside.
3. A separate 570 km² Grafton "ring-fence" existed briefly and was **removed** —
   the routed boundary now runs west of the city instead, achieving the same
   result without a bolt-on polygon.
4. The southern edge was a straight line due east at 29.8073 S until it too was
   **road-routed**. 29.8073 S remains the nominal latitude and the geometric
   version of the line is kept; the operative edge follows roads and stays within
   about 5 km either side of it.
5. **Casino was folded in** (this revision) behind a 5 km road-routed boundary,
   as one continuous area rather than a detached ring. That closes open question
   1 below for Casino; Kyogle is untouched and still outside.
6. **Every polygon is now held 500 m south of the NSW/QLD border**, measured
   against the **OpenStreetMap administrative boundary** rather than the 1:250k
   state outline the rest of the build uses. The old line ran a median 109 m and
   up to 6 km from the real border, so a setback measured against it did not mean
   what it said. Before this, Open Area 2 spilled 0.42 km² into Queensland.

## 3. Where the boundaries actually run

**Open Area 1**, west to east: Gwydir Hwy near the SA corner → Sunraysia mallee
(geometric) → Swan Hill → Deniliquin → Wagga corridor (fully on roads) →
Kosciuszko high country (geometric) → Cape Howe (geometric).

573 km of it follows real roads. The rest holds the geometric line because no
connected public road network exists within 12 km there.

**Open Area 2**, south to north: west of Grafton → Summerland Way corridor →
Casino–Coraki Road → Bruxner Hwy → Kyogle Road → Nimbin Road → Routes 32/34 →
Queensland border near Murwillumbah. 168 km on roads, 13 km on the line.

**Open Area 1's Deniliquin detour**, south to north to east: Melvilles Rd →
Taylors Bridge Rd → Gulpa Creek Rd → Walliston Rd → **Cobb Hwy** north from
Mathoura → *a true 5 km arc across the west and north* → Cobb Hwy → Mavers Rd →
Atkinsons Lane → Lawrence Rd → Conargo Rd → Claremont Lane → Lawson Lane →
Aratula North Rd → **Riverina Hwy** → Tocumwal Rd → Gollops Rd. 80.2 km,
replacing 32.2 km. 6 of 11 legs on road. **Deniliquin has no orbital road** — its
roads are dead-end radials, so with the town core excluded there is no connected
path at all around the west and north, at any radius. That is why five legs hold
the geometric circle rather than a road. Closest approach to the town centre
4.99 km.

**Open Area 2's Casino detour**, south to north: Tatham Ellangowan Rd →
Ellangowan Rd → Johnsons Rd → Summerland Way → Vouts Rd → Llewellyns Rd →
Bruxner Hwy → Taylors Lane → Sextonville Rd → Reynolds Rd → Savilles Rd →
Manifold Rd → Naughtons Gap Rd. 46.6 km, replacing 56.4 km of switchbacks east
of the town. 6 of 9 legs on roads; the three short western arcs keep the
geometric chord, ~170 m inside the 5 km circle. Closest approach to the town
centre 4.74 km.

**Open Area 2's southern edge**, west to east: McCarthys Rd → Armidale Rd →
Braunstone Rd → Orara Way → Poley House Rd → Dinjerra Rd → Big River Way →
Pacific Hwy → Franklins Rd → Lookout Rd → Stonehouse Rd → Lloyds Rd → Wooli Rd →
Coast Range Rd → Wooli Rd → Diggers Camp Rd, meeting the sea at Diggers Camp.
65.1 km total, 57.5 km on roads, 7.7 km on the line (two legs found no
acceptable road path). 8 of 10 legs routed. Between 153.03 and 153.06 E the
boundary follows a southward loop of the Pacific Hwy and Lookout Rd, leaving a
narrow tongue about 5 km below the nominal line near Glenugie; it encloses no
locality, but it is the least tidy part of the boundary.

### Which towns fall where

**Open Area 1 (in):** Albury, Moama, Tocumwal, Corowa, Barham, Mulwala, Howlong,
Barooga, Euston, Buronga, Dareton, Tooleybuc, Mathoura, Khancoban.

**Open Area 1 (out, and notable):** Culcairn 36.4 km, Berrigan 27.2, Holbrook
25.9, Finley 18.0, Eden 40.9, Jindabyne 41.7, Bombala 30.5 — all of these *were*
inside at 50 km. **Deniliquin (34.9 km) is now in**, behind its own 5 km boundary,
and brought Deniliquin North and Cornalla with it on both versions and Tuppal on
the routed one.

**Mathoura** is `open` geometrically but `active` on the routed boundary — it is
8.2 km from the border, inside the 15 km line, but the routed line runs north of
it. That predates the Deniliquin work; the "in" list above is the geometric one.

**Open Area 2 (in):** Grafton, South Grafton, Junction Hill, Clarenza, Waterview
Heights, Ulmarra, Maclean, Yamba, Iluka, Evans Head, Woodburn, Coraki, Ballina,
Alstonville, Lennox Head, Byron Bay, Bangalow, Mullumbimby, Brunswick Heads,
Ocean Shores, Lismore, Nimbin, Murwillumbah, Kingscliff, Tweed Heads.

**Open Area 2 (out):** Copmanhurst, Coutts Crossing, Kyogle (54 km from coast,
27 km from Casino), Wooli, Coffs Harbour. Routing the southern edge moved
**Mcphersons Crossing** and **Pillar Valley** out. Folding in Casino moved
**Casino**, Greenridge, Irvington, Spring Grove, Tomki and Wooroowoolgan in on
both versions, and **Naughtons Gap** and **Yorklea** in on the routed version
only.

4,118 localities are classified in `data/towns.json`. On the operative
**road-routed** boundaries: 111 in Open Area 1, 336 in Open Area 2, 1,433 Active
PMA, 2,238 Victorian (context only). On the geometric boundaries: 113 / 328 /
1,439. Each locality carries both — `zr` is routed, `z` is geometric.

## 4. Open questions for the business

These are decisions nobody has made yet. They are not bugs.

1. **Kyogle sits outside Open Area 2** at 54 km from the coast — 19 km beyond the
   35 km rule and 27 km from Casino, so the Casino detour does not reach it. If
   Kyogle is meant to be in, it needs either its own treatment (the Casino method
   would work) or an anchor distance of ~55 km, which would redraw the whole
   strip. **Casino was resolved in favour of inclusion** and is now inside.
2. ~~Deniliquin outside Open Area 1~~ — **resolved**: it is now inside behind a
   5 km road-routed boundary. Culcairn (36.4 km), Berrigan (27.2) and Holbrook
   (25.9) are the nearest remaining towns that were inside at 50 km; none has
   been asked for.
3. **Open Area 2's southern edge** is now routed on roads around the nominal
   29.8073 S, which sits ~13 km south of Grafton's centre. 29.8073 S was chosen
   as the minimum latitude that encloses the whole built-up area. If a cleaner
   single feature is wanted for the southern edge — the Clarence River, an LGA
   boundary, or one named road end to end — say which and it can be redrawn.
4. **Which boundary version is contractual** — the road-routed one or the
   geometric one. They differ by under 1% in area but by up to several kilometres
   in places.
5. The **Jindabyne → Cape Howe** section of Open Area 1 was never road-routed
   (see limitations). It is geometric by default, not by decision.

## 5. How it is built

```
fetch data ──► compute geometry ──► route on roads ──► build map ──► encrypt
```

```bash
pip install -r scripts/requirements.txt
make            # everything
make data       # download the source datasets
make geometry   # borders, buffers, town classification, overview PNG
make map        # inline MapLibre + GeoJSON into one HTML file
make lock PW=malsyd
```

| Script | Does |
|---|---|
| `fetch_data.sh` | Downloads state boundaries, Natural Earth roads, locality coordinates, MapLibre |
| `build_geometry.py` | Border extraction, 15 km buffer, Open Area 1 geometric |
| `build_oa1_road_route.py` | Assembles Open Area 1's routed boundary from the corridor route files |
| `build_open_area_2a.py` | Coastline extraction, Grafton distance, 35 km buffer |
| `build_open_area_2.py` | Open Area 2 routed western boundary and area arithmetic |
| `build_oa2_south_route.py` | Open Area 2 routed **southern** edge; rewrites `open2_road`, `active_road` and every locality's `zr` |
| `build_oa1_deniliquin.py` | Splices the **Deniliquin** detour into Open Area 1's routed boundary; rewrites `open_road`, `open_exact`, `line_snap`. Runs **before** the Casino script |
| `build_oa2_casino_border.py` | Splices the **Casino** detour into Open Area 2's western boundary, applies the **500 m QLD border setback** to all four polygons, recomputes the Active PMA and rewrites `z` and `zr` |
| `build_towns.py` | Classifies 4,118 localities by zone and distance |
| `build_overview.py` | The state overview PNG |
| `build_map.py` | Inlines everything into the single-file map |
| `encrypt.py` | AES-256-GCM password gate |
| `verify_map.py` | Asserts every layer loads and reports which hosts the page contacts |

### The road routing, in one paragraph

The geometric line is sampled every 4 km. Anchors are taken every 1–3 samples and
snapped to the nearest OpenStreetMap road node. Consecutive anchors are joined by
**Dijkstra shortest paths along road centrelines**. A leg is accepted only if both
anchors are within 12 km of the network and the routed distance is under 2.6× the
direct distance plus 8 km; otherwise that section keeps the geometric line. This
is why the boundary follows real roads rather than cutting chords between snapped
points, and why it honestly reverts to the line in roadless country.

Anchor spacing matters: at 12 km spacing the Open Area 2 route shortcut through
Grafton on the Summerland Way. It needed 4 km spacing to hold west of the city.

## 6. Data sources

| Dataset | Source | Licence |
|---|---|---|
| State boundaries | `rowanhogan/australian-states` (GitHub) | Open |
| Road network | **OpenStreetMap via Overpass API** | ODbL |
| Coarse roads (legacy) | Natural Earth 10m | Public domain |
| Localities + coordinates | `matthewproctor/australianpostcodes` | Open |
| Base map | OpenFreeMap (Liberty / Positron), OpenMapTiles schema | ODbL |
| Imagery | Esri World Imagery | Esri terms |
| Map library | MapLibre GL JS 4.7.1 | BSD-3 |

All projections and distances are computed in **GDA94 / Geoscience Australia
Lambert (EPSG:3112)**, output as WGS84.

## 7. Base map and keys

The map is **vector** (MapLibre + OpenFreeMap) and needs **no API key**. Satellite
is Esri raster imagery, also keyless.

If the vector style is unreachable the map falls back to imagery and says so on
screen rather than going blank.

> **A CARTO key was used in an earlier build and has been removed.** CARTO now
> requires a key and stamps `API KEY REQUIRED` across unkeyed tiles. The parameter
> is `?key=`, not `?api_key=` — that mistake cost a build. If you ever go back to
> CARTO, set `CARTO_API_KEY` at the top of `scripts/template.html`.
>
> The old key `cb1_2tyi_1_148a4751e35ac61e4421aef0` appears in this repo's **git
> history**. It is no longer live in any file, but rotate it in the CARTO console
> if it still exists on the account.

## 8. Password

`index.html` is AES-256-GCM encrypted, key derived by PBKDF2-HMAC-SHA256 at
250,000 iterations. Current password: **`malsyd`**.

Change it with `make lock PW=newpassword`, then commit `index.html`.

The unprotected copy lives in `local/` and is git-ignored. Keep it that way —
committing it defeats the password.

## 9. Known limitations

1. **Jindabyne → Cape Howe (~170 km)** of Open Area 1 was never road-routed. The
   Overpass mirrors returned dispatcher timeouts on every attempt for that
   corridor. The routing code works; it just needs the data through.
2. **Overpass mirrors are unreachable from the sandbox and rate-limit in the
   browser.** Neither shell can reach them at all; the working method is to open
   `https://overpass.kumi.systems/` in a browser pane and `fetch()` the query
   from inside that page, then run the graph build and Dijkstra routing there and
   bring back only the polyline. Expect 40–60 s per large corridor query and
   60–120 s between them.
3. The **locality coordinates** come from a postcode dataset. A few are offset by
   10–20 km from the true town centre (Wentworth is the worst). Classification
   near a boundary should be spot-checked against a real address.
4. **State boundary resolution** is ~1:250k. Fine for a concept map; not survey
   grade. Any boundary going into an agreement should be checked against a
   surveyed description.
5. The map has not been rendered against the live vector tiles in this build
   environment — the sandbox has no route to the tile servers. The style URL was
   verified to return a valid MapLibre v8 style; the composed page renders on a
   normal connection. All twelve custom layers were confirmed to load in headless
   Chromium with the tile requests failing.
6. **`assets/state-overview.png` predates the routed southern edge.** The change
   is 64 km² out of 787,000 and invisible at state scale, but the PNG has not
   been regenerated (`build_overview.py` needs the full `work/` dataset).

## 10. Deliverables

| File | What |
|---|---|
| `index.html` | The map, password-protected. Open in any browser. Nothing to install. |
| `local/map-unlocked.html` | Same map, no password. Git-ignored. |
| `assets/state-overview.png` | Static one-page overview with a Northern Rivers inset |
| `data/pma.geojson` | All boundaries and areas, WGS84 |
| `data/towns.json` | 4,118 localities classified |
| `data/oa2_route.txt`, `data/oa2_south_route.txt`, `data/oa1_route*.txt` | The raw routed road boundaries |
| `docs/METHODOLOGY.md` | Full method, spot checks, every known limitation |
| `README.md` | Setup, publishing, data sources |

## 11. Publishing

GitHub Pages: **Settings → Pages → Deploy from branch `main`, folder `/ (root)`**.
`.nojekyll` is present. The map goes live behind the password.

If the repo is public, note that `data/` exposes the boundaries in plain text even
though `index.html` is encrypted. Make the repo private, or delete `data/` and
`scripts/` before pushing — `index.html` is self-contained and won't break.

---

*Concept map. Boundaries indicative. Not a legal instrument.*
