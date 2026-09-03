# Methodology

## Coordinate system

All measurement is done in **GDA94 / Geoscience Australia Lambert
(EPSG:3112)** — an equal-area-ish conformal projection appropriate for
continental Australia. Output is reprojected to WGS84 (EPSG:4326) for display.

## The border

The NSW/VIC border is extracted as the shared boundary between the two state
polygons. The source data splits it into five segments (small topological gaps
where the polygons don't quite meet along the Murray); all five are used, which
is what makes the far-western section around Wentworth, Buronga and Dareton
measure correctly.

Total length: **1,753 km**.

## Open Area 1 — the 50 km strip

A 50 km buffer is taken around the border line and intersected with the NSW
polygon. Distance is **perpendicular to the border**, which is the standard
reading for a territory strip — not 50 km of latitude due north.

Result: **53,596 km²**.

The strip's mean width works out at ~31 km when you divide area by border
length. That is not an error — the Murray meanders heavily, so the border is
1,753 km long while spanning only ~800 km west to east.

## Open Area 1 — road-snapped variant

The 50 km offset line is sampled every 10 km and each sample is snapped to the
nearest mapped road within 25 km; samples with no road in range keep their exact
position. The resulting line is simplified and used to split the NSW polygon.

Result: **54,623 km²** — within 2% of the exact strip.

### Known limitation

This variant is built from **Natural Earth's 1:10m road network**, which
contains only major highways and carries no road names for Australia. The
median distance from the 50 km line to the nearest mapped road is 22 km, so the
snapped boundary is *indicative of the corridor*, not a surveyed alignment.

A production version should be rebuilt against OpenStreetMap (Overpass) or the
NSW Digital Topographic Database, which would also allow the boundary to be
written up by road name — "follows the Riverina Highway to X, then the Olympic
Highway to Y".

## Locality classification

Localities come from the Australian postcode dataset, using the per-locality
`Lat_precise` / `Long_precise` fields rather than postcode centroids (postcode
centroids collapse dozens of Riverina localities onto a single point). Each NSW
locality within 200 km of the border is tagged `open` or `active` by
point-in-polygon test, with its perpendicular distance to the border.

## Spot checks

| Town | Distance to border | Zone |
|---|---|---|
| Albury | 1.4 km | Open |
| Moama | 1.2 km | Open |
| Tocumwal | 1.0 km | Open |
| Finley | 18.0 km | Open |
| Holbrook | 25.9 km | Open |
| Bombala | 30.5 km | Open |
| Deniliquin | 34.9 km | Open |
| Culcairn | 36.4 km | Open |
| Eden | 40.9 km | Open |
| Moulamein | 41.9 km | Open |
| Jerilderie | 53.1 km | Active |
| Henty | 53.2 km | Active |
| Urana | 72.7 km | Active |
| Wagga Wagga | 92.6 km | Active |
| Hay | 136.3 km | Active |

Two worth noting: **Deniliquin** falls inside the open area at 34.9 km because
the Murray bends north at Mathoura, and **Eden** falls inside at 40.9 km off the
straight Cape Howe survey line — both read as "further away" than they measure.

## Client-side calculations

The map's point-check recomputes distance to the border in the browser using a
local planar approximation of the great-circle distance. It agrees with the
projected Python calculation to within ~0.5 km at the scales involved
(Deniliquin: 34.5 km in-browser vs 34.9 km projected).

---

# Open Area 2 — the Northern Rivers strip

## The rule

1. **Southern edge** — a straight line due east from Grafton (152.9336 E,
   29.6876 S) to the coast. That line is **37.4 km** long and meets the sea near
   Minnie Water.
2. **Anchor distance** — Grafton's perpendicular distance to the nearest
   coastline is **35.0 km**. That distance sets the width of the strip.
3. **Western edge** — held at 35.0 km from the coast, following the coastline
   north all the way to the Queensland border.

Result: **6,069 km²**.

## Road-snapped variant

Unlike Open Area 1, this one is built on **real OpenStreetMap data**. A corridor
polygon 18 km either side of the 35 km line was queried through the Overpass API
for `motorway|trunk|primary|secondary` ways, returning 1,454 road segments.

The 35 km line is sampled every 4 km (42 samples). Each sample snaps to the
nearest point on any of those roads; samples more than 8 km from a road keep
their exact position rather than being dragged off-corridor. **39 of 42 samples
landed on a road**, mean snap distance 2.4 km.

Result: **6,072 km²** — 0.05% different from the exact strip.

### The route, south to north

| Road | Section |
|---|---|
| Gwydir Highway (B76) | at Grafton |
| **Summerland Way (B91)** | Grafton north to near Casino — the long run, 18 of 42 samples |
| Casino–Coraki Road | around Casino |
| Bruxner Highway (B60) | brief east–west section |
| Spring Grove Road | |
| **Kyogle Road** | |
| Rock Valley Road, Nimbin Road | |
| **Route 32** | Nimbin north toward Uki |
| Route 34, Route 97 | to the Queensland border near Murwillumbah |

## Spot checks

| Town | Distance from coast | Zone |
|---|---|---|
| Ballina | 0.9 km | Open Area 2 |
| Evans Head | 1.2 km | Open Area 2 |
| Byron Bay | 1.4 km | Open Area 2 |
| Yamba | 2.3 km | Open Area 2 |
| Tweed Heads | 4.5 km | Open Area 2 |
| Alstonville | 8.2 km | Open Area 2 |
| Maclean | 13.9 km | Open Area 2 |
| Coraki | 17.5 km | Open Area 2 |
| Murwillumbah | 18.3 km | Open Area 2 |
| Lismore | 24.0 km | Open Area 2 |
| Nimbin | 32.7 km | Open Area 2 |
| **Grafton** | **35.2 km** | **on the boundary** |
| Casino | 43.2 km | Active |
| Kyogle | 54.2 km | Active |

Casino and Kyogle fall outside by 8 km and 19 km respectively — worth confirming
that is the intent, since both are commercially significant for the Northern
Rivers.

Grafton measures 35.2 km against an anchor distance of 35.0 km, so it lands
0.2 km outside its own boundary. It is marked on the map as an anchor rather
than being assigned to a zone.

---

# Base mapping

CARTO raster basemaps, keyed. The key goes on the tile URL as `?key=`.

An earlier build used `?api_key=`, which CARTO silently ignores — the tiles
still returned HTTP 200 and a valid PNG, but with an `API KEY REQUIRED`
watermark burnt into the image. Checking the status code is not enough; the
tile has to be looked at. The verification script
(`local/verify_key.py` pattern) asserts every `cartocdn` request carries
`?key=`, and a tile was pulled and inspected by eye.

---

# Revision — 15 km Open Area 1, and the Grafton ring-fence

## Open Area 1 reduced to 15 km

The strip is now **15 km** perpendicular from the Victorian border: **17,670 km²**,
down from 53,600 km² at 50 km. Towns that were inside at 50 km and are now outside
include Deniliquin (34.9 km), Culcairn (36.4), Berrigan (27.2), Holbrook (25.9),
Finley (18.0), Moulamein (41.9), Eden (40.9), Jindabyne (41.7) and Bombala (30.5).
Still inside: Albury, Moama, Tocumwal, Corowa, Barham, Mulwala, Howlong, Barooga,
Euston, Buronga, Dareton, Tooleybuc, Mathoura (8.2) and Khancoban (7.9).

**The road-snapped variant of Open Area 1 is not in this build.** The Overpass
mirrors repeatedly returned dispatcher timeouts on the long border corridors, and
the previous Natural Earth fallback is too coarse to snap a 15 km line against —
its median distance to a mapped road is 14.5 km, which would move the boundary
by as much as the strip is wide. Only the exact 15 km line is published.

## Grafton ring-fence

Built from real OpenStreetMap data: 1,402 ways within 15 km of Grafton
(motorway → residential). The city's extent is taken from the residential road
network; 20 anchors are placed one sector-radius plus 3 km out from the centroid,
snapped to the nearest road node, and consecutive anchors are joined by Dijkstra
shortest paths **along road centrelines**, with a 12× cost penalty on edges inside
the urban core so routes go around the city rather than through it. All 20 legs
routed successfully.

The published ring-fence is the **convex hull of that routed loop** — 570 km²,
88 km perimeter, every vertex sitting on a real road.

### Why the hull rather than the loop itself

Grafton straddles the Clarence River and the only road crossings are the bridges
in the city itself. A closed loop that stays on roads therefore cannot enclose
both banks — it has to come back through town to cross, which splits the enclosed
area and leaves South Grafton outside. Two routing attempts confirmed this, the
second with the urban-core penalty in place. The hull is the honest compromise:
its vertices are road positions, its edges are chords between them.

Inside: Grafton, South Grafton, Junction Hill, Clarenza, Great Marlow,
Waterview Heights, Ulmarra. Outside: Copmanhurst, Coutts Crossing.
