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
reading for a PMA strip — not 50 km of latitude due north.

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

### Road-routed variant

Built from OpenStreetMap. The 15 km line is split into five corridors, each
queried through Overpass for `motorway|trunk|primary|secondary|tertiary|unclassified`
ways within 11 km. Anchors are placed every ~24 km along the line, snapped to the
nearest road node, and consecutive anchors joined by **Dijkstra shortest paths along
road centrelines** — not chords between snapped points. A leg is only accepted if
both anchors are within 12 km of the network and the routed distance is under
2.6x the direct distance plus 8 km; otherwise that section keeps the geometric line.

Result: **17,545 km²**, within 0.7% of the exact 17,670 km².

| Corridor | On roads | On the geometric line |
|---|---|---|
| SA corner → Swan Hill | 159 km | 179 km |
| Swan Hill → Deniliquin | 149 km | 23 km |
| Deniliquin → Wagga | 175 km | 0 km |
| Wagga → Jindabyne | 90 km | 78 km |
| Jindabyne → Cape Howe | 0 km | ~170 km |

The line sections are not a shortcut — they are where no connected public road
network exists within 12 km of a line 15 km off the border: the Sunraysia mallee,
the Kosciuszko high country, and the Coolangubra/Nalbaugh forests behind Cape
Howe. Dragging the boundary onto the nearest mapped road in those places would
move it by more than the strip is wide.

The final corridor (Jindabyne → Cape Howe) also could not be fetched — the
Overpass mirrors returned dispatcher timeouts on every attempt — so it is on the
geometric line for both reasons.

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

---

# Revision — Open Area 2 routed, Grafton folded in

Open Area 2's western boundary is now built the same way as Open Area 1:
shortest-path routing along OpenStreetMap road centrelines.

- 2,930 road ways queried along a 12 km corridor
- Anchors every 4 km (not 12 km — the wider spacing let the route shortcut
  through Grafton on the Summerland Way)
- **41 of 44 legs routed on roads**: 168 km on roads, 13 km on the geometric line

Result: **6,590 km²**, against 6,545 km² for the geometric 35 km line.

## Grafton, without a ring-fence

The separate 570 km² ring-fence is gone. Instead the routed boundary itself runs
west of the city and the southern edge sits at **29.8073 S** — below the whole
built-up area — so Grafton falls inside as a consequence of the boundary rather
than as a bolt-on.

| Locality | Road-routed | Geometric 35 km |
|---|---|---|
| Grafton | **In** | out |
| South Grafton | **In** | out |
| Junction Hill | **In** | out |
| Clarenza | **In** | In |
| Waterview Heights | **In** | out |
| Ulmarra | **In** | In |
| Copmanhurst | out | out |
| Coutts Crossing | out | out |
| Casino | out | out |
| Kyogle | out | out |

This also resolves the Clarence River problem from the earlier build. A closed
loop around the city could not stay on roads because the only crossings are the
bridges in town. An open boundary that passes west of the city has no such
constraint — it never needs to cross the river at all.

## Wording

"Territory" has been removed throughout. The blue area is the **Active PMA**;
the two carve-outs are **Open Area 1** and **Open Area 2**.

---

# Revision — Open Area 2's southern edge routed on roads

Until this revision the southern edge of Open Area 2 was the one part of either
open area still drawn as a pure straight line: due east at **29.8073 S**, from
the southern terminus of the routed western boundary (152.8899 E) to the sea
near Minnie Water — 38.3 km of latitude with no reference to anything on the
ground. It is now routed the same way as every other boundary in the project.

## Method

Identical parameters to the rest of the build, deliberately:

- OpenStreetMap ways of class `motorway` … `residential` were queried through
  Overpass for a corridor 152.76–153.48 E, 30.02–29.60 S — **2,105 ways,
  21,451 graph nodes, 21,927 edges**.
- The straight line is sampled every **4 km** (11 samples).
- Each sample snaps to the nearest road node within **12 km**. All eleven
  snapped, the worst at 1.6 km, the median at 0.7 km.
- Consecutive anchors are joined by **Dijkstra shortest paths** along road
  centrelines, accepted only where the routed distance is under
  **2.6 × direct + 8 km**.
- **8 of the 10 legs routed on roads.** The two that did not — 152.97–153.01 E
  and 153.05–153.09 E — keep the geometric line, as elsewhere in the project.
- Immediate out-and-back retraces (an anchor landing on a dead-end spur) are
  collapsed, and the assembled line was checked for self-intersection before it
  was used to cut the polygon.

## The route, west to east

McCarthys Road → Armidale Road → Braunstone Road → Orara Way → Poley House Road
→ Dinjerra Road → Big River Way → Pacific Highway → Franklins Road → Lookout
Road → Stonehouse Road → Lloyds Road → Wooli Road → Coast Range Road → Wooli
Road → Diggers Camp Road, reaching the sea at **Diggers Camp**
(153.2882 E, 29.8137 S).

**65.1 km** of boundary in place of a 38.3 km line: **57.5 km on roads**,
7.7 km still on the geometric line. The road grain in this corridor runs
north–south — the Pacific Highway, the Big River Way, the Orara Way — so an
east–west boundary has to work across it. The route stays within **5.3 km north
and 5.1 km south** of 29.8073 S throughout.

One consequence worth naming: between 153.03 and 153.06 E the boundary follows a
southward loop of the Pacific Highway and Lookout Road, leaving a narrow tongue
of Open Area 2 reaching about 5 km below the nominal line near Glenugie. It
encloses no locality. It is a real road corridor, not an artefact of the
algorithm, but it is the least tidy part of the boundary.

## Effect

| | Before | After |
|---|---|---|
| Open Area 2 — road-routed | 6,590 km² | **6,526 km²** |
| Open Area 2 — geometric | 6,545 km² | 6,545 km² (unchanged) |
| Active PMA — road-routed | 763,578 km² | **763,642 km²** |

Two localities change side, both from Open Area 2 to the Active PMA:
**Mcphersons Crossing** and **Pillar Valley**. Everything else holds, including
the whole of Grafton, Braunstone, Bom Bom, Lake Hiawatha, Minnie Water and
Diggers Camp. Coutts Crossing, Glenugie and Wooli remain outside, as before.

The geometric version of the southern edge is retained as
`open2_line_south_exact` and still draws on the map under **Geometric lines**;
the routed edge is `open2_line_south` and draws with the road boundaries.

## Reproducing it

`scripts/build_oa2_south_route.py` reads `data/oa2_south_route.txt` (the routed
polyline) together with `data/oa2_route.txt` (the western boundary), joins them
into a single cut, splits New South Wales with it and rewrites `open2_road`,
`active_road` and the `zr` field on every locality. The routing itself is done
against live Overpass data; the sandbox has no route to the Overpass mirrors, so
the query and the Dijkstra pass are run in a browser page on the Overpass origin
and only the resulting polyline is brought back — the same workaround used for
the western boundary.
