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

---

# Revision — Casino folded in, and a 100 m setback from the Queensland border

Two changes, both requested by the business.

## 1. Casino inside Open Area 2, behind a 5 km road-routed boundary

Casino is **43.6 km from the coast** — 8 km outside the 35 km strip — and was
listed as an open question in every earlier handover. It is now inside.

A detached 5 km ring was rejected: the project already removed one bolt-on
polygon (the 570 km² Grafton ring-fence) and would have reintroduced the same
problem. Instead the **western boundary of Open Area 2 detours around Casino**
and rejoins the corridor north and south, so Open Area 2 remains one continuous
area.

### Method

The routing parameters match the rest of the project, with one addition.

- OpenStreetMap ways of class `motorway` … `residential` were queried through
  Overpass for 152.80–153.38 E, 29.12–28.60 S — **3,846 ways, 45,348 graph
  nodes, 46,249 edges**.
- Anchors are placed on the **5 km circle around the town centre**
  (153.048 E, 28.861 S) every 30° of arc — about 2.6 km apart, tighter than the
  project's usual 4 km because the radius is small — from bearing 160° round the
  west to bearing 10°, plus the two attachment points on the existing boundary.
- Each anchor snaps to the **nearest road node that is itself at least 5 km from
  Casino**, so no anchor sits inside the ring. All ten snapped, the worst at
  1.1 km; every anchor landed 5.1–6.1 km from the town centre.
- **Road nodes within 4.2 km of the town centre are deleted from the graph before
  routing.** Without this, the sparse road network west of Casino sent three of
  the shortest paths straight back through the middle of town — the routed
  boundary passed within 160 m of the town centre. With it, the closest approach
  is **4.74 km**.
- Consecutive anchors are joined by Dijkstra shortest paths, accepted under the
  usual 2.6 × direct + 8 km rule. **6 of 9 legs routed on roads**; three short
  arcs on the western side keep the geometric chord, which cuts about 170 m
  inside the 5 km circle.

### The detour, south to north

Tatham Ellangowan Road → Ellangowan Road → Johnsons Road → Summerland Way →
Vouts Road → Llewellyns Road → Bruxner Highway → Taylors Lane → Sextonville Road
→ Reynolds Road → Savilles Road → Manifold Road → Naughtons Gap Road.

**46.6 km**, replacing 56.4 km of the old boundary — the detour is shorter than
what it replaces, because the old line wandered through a series of tight
switchbacks east of Casino. It leaves the old boundary at 29.0136 S, 153.0716 E
and rejoins it at 28.7928 S, 153.1132 E.

### The geometric version

The geometric rule becomes: **within 35 km of the coast, or within 5 km of
Casino, or in the corridor joining the two** — the corridor being the convex hull
of the 5 km disc and the nearest 8 km window of the 35 km band, which produces the
two natural tangent lines. That takes the geometric area from 6,545 km² to
**6,713 km²**: 79 km² for the disc itself and 89 km² for the neck.

### Who moves

Eight localities join Open Area 2: **Casino**, Greenridge, Irvington, Spring
Grove, Tomki, Wooroowoolgan (all in both versions), and Naughtons Gap and Yorklea
(routed version only). **Kyogle stays out** at 54 km from the coast and 27 km from
Casino — it was the other half of the original open question and nothing in this
change reaches it.

## 2. Every polygon held 500 m south of the real Queensland border

### The border itself was wrong first

The setback is only as good as the line it is measured from, and the line this
project had was not the border people see on a map. Every polygon was derived
from `states.geojson`, whose NSW/QLD boundary is **313 vertices over 1,501 km** —
a ~1:250k generalisation that cuts the corner off every meander of the Dumaresq,
Macintyre and Barwon.

The border is now taken from **OpenStreetMap's administrative boundary**: the ways
shared by the `admin_level=4` relations for New South Wales and Queensland, which
is the same official line consumer maps render. Simplified to 20 m it is
**4,845 vertices over 1,681 km** — 180 km longer, because it actually follows the
rivers.

How far apart they are, measured from the real border to the old line:

| | |
|---|---|
| median | 109 m |
| mean | 150 m |
| 95th percentile | 377 m |
| more than 100 m apart | 52.9% of the border |
| more than 250 m apart | 18.1% |
| more than 500 m apart | 0.7% |

A 100 m setback measured against the old line was therefore inside the error of
the line itself. Measured against the real border, 500 m is a real 500 m.

*Licensing note: Google's boundary data is proprietary and was not used. The
OpenStreetMap administrative boundary is the same underlying official border,
under ODbL — already a data source in this project.*

### The clip

Every PMA polygon now goes through one clip:

1. intersect with New South Wales ∪ the ACT;
2. intersect with **everything south of the real border** — NSW ∪ ACT is split by
   the OSM line and only the southern side is kept, so no polygon can survive
   north of it even where the 1:250k outline bulges across;
3. subtract Queensland outright;
4. subtract a **500 m buffer of the border**;
5. drop any fragment under **5 hectares**;
6. re-validate, in both EPSG:3112 and WGS84 (a polygon valid in the projected CRS
   can pinch into a self-intersection once reprojected).

The 5 km of border east of Point Danger is maritime — the boundary continues out
to sea — and is trimmed, since the PMA ends at the coast.

Before this work Open Area 2 spilled **0.42 km² into Queensland** and the Active
PMA **0.017 km²**, in slivers where the published NSW and Queensland polygons
overlap each other around Tweed Heads.

**Verification:** 1,681 points sampled at 1 km intervals along the border, each
tested at 100, 250, 400 and 450 m to the south. **No PMA polygon contains any of
them.** The first samples fall inside at 600 m. Measured minimum clearance from
the border line to the nearest polygon edge is **498.8 m**, and the area of every
polygon inside Queensland is **zero**.

The border is published as `qld_border` in `data/pma.geojson` and draws on the map
with the Victorian border under the **State borders** toggle.

> Note the two borders in this project are now at different resolutions: the
> Queensland border is the OSM administrative line, the Victorian border is still
> the 1:250k outline. Open Area 1 was not in scope for this change. If the same
> treatment is wanted on the Murray, it is the same method.

## Effect

| | Before | After |
|---|---|---|
| Open Area 2 — road-routed | 6,526 km² | **6,754 km²** |
| Open Area 2 — geometric | 6,545 km² | **6,696 km²** |
| Active PMA — road-routed | 763,642 km² | **763,006 km²** |
| Active PMA — geometric | 763,497 km² | **762,937 km²** |
| Open Area 1 | 17,545 / 17,671 km² | unchanged |

Open Area 2 gains 228 km² net: about 394 km² for Casino, less what the setback
gives up along the border. Across all zones the 500 m setback removes 408 km² —
well under the naive 1,681 km × 500 m, because the border meanders tightly enough
that the buffer overlaps itself through most of the river sections.

## Reproducing it

`scripts/build_oa2_casino_border.py` reads `data/oa2_casino_route.txt` (the routed
detour), splices it into `data/oa2_route.txt` to produce
`data/oa2_route_casino.txt`, cuts New South Wales with the combined boundary,
applies the border clip to all four polygons and rewrites every locality's `z`
and `zr`. It reads the border from `data/qld_border.geojson`, which
`scripts/decode_qld_border.py` produces from `data/qld_border.enc` — the Overpass
result carried out of the browser as a delta-encoded polyline and verified by
checksum on arrival. The Overpass query and the Dijkstra pass run in a browser page on the
Overpass origin, as for the other routed boundaries.

---

# Revision — Deniliquin folded into Open Area 1

Deniliquin sits **34.9 km north of the Victorian border** — nearly 20 km outside
the 15 km strip — and has been an open question in every handover since the rule
was cut from 50 km to 15 km. It is now inside, on the same terms as Casino: the
routed boundary detours around the town and rejoins the corridor east and west,
so Open Area 1 stays one continuous area rather than gaining a bolt-on ring.

## Deniliquin has no orbital road

This is the one place the Casino method could not be applied unchanged, and the
reason is a fact about the town rather than a choice.

Casino has a rough ring at 5 km — Ellangowan Road, Johnsons Road, Vouts Road,
Llewellyns Road — so excluding the town core from the graph still left a
connected path around it. Deniliquin does not. Its roads are dead-end radials off
the centre, and with the core excluded there is **no connected path at all**
around the west and north side. Not a long one; none. Unconstrained Dijkstra
returns no route between five consecutive pairs of ring anchors.

Nor does widening help. Testing complete 12-arc rings at every radius:

| radius | arcs on road |
|---|---|
| 5 km | 5 of 12 |
| 8 km | **9 of 12** |
| 10 km | 7 of 12 |
| 12 km | 7 of 12 |
| 15 km | 7 of 12 |
| 20 km | 7 of 12 |

No radius closes the ring. 8 km is the best available anywhere and still leaves
three gaps.

So the boundary does what this project already does in the Sunraysia mallee and
the Snowy high country: **follows roads where roads exist, and holds the
geometric line where they do not.** Six of eleven legs route on road; the five
across the west and north hold a **true 5 km circular arc**, densified every 3°,
rather than a chord between anchors — so the 5 km rule is honoured exactly there
rather than approximately.

## Method

Same parameters as Casino, with the arc fallback added.

- OpenStreetMap ways of class `motorway` … `residential` for 144.45–145.60 E,
  36.00–35.30 S — **2,547 ways, 21,472 graph nodes, 22,360 edges**.
- Anchors on the **5 km circle** around the town centre (144.95658 E,
  35.52824 S) every 30° of arc, from bearing 190° round the west and north to
  bearing 100°, plus two attachment points on the existing boundary.
- Each anchor snaps to the nearest road node **at least 5 km from the town**; all
  twelve snapped, the worst at 1.6 km, every one landing 5.0–6.0 km out.
- Road nodes within **4.2 km of the centre** are deleted from the graph, so no
  shortest path can cut back through Deniliquin.
- Legs joined by Dijkstra under the usual 2.6 × direct + 8 km rule; where no
  route exists, the 5 km arc is held.
- The assembled line is de-spiked, one self-intersection loop excised, and
  checked simple before it is used to cut the state.

Closest approach of the finished boundary to the town centre: **4.99 km**
(routed) and **5.00 km** (geometric).

## The detour, south to north to east

Melvilles Road → Taylors Bridge Road → Gulpa Creek Road → Walliston Road →
**Cobb Highway** (north from Mathoura) → *5 km arc across the west and north* →
Cobb Highway → Mavers Road → Atkinsons Lane → Lawrence Road → Conargo Road →
Claremont Lane → Lawson Lane → Aratula North Road → **Riverina Highway** →
Tocumwal Road → Gollops Road.

**80.2 km**, replacing 32.2 km of the old boundary. It leaves at 35.7392 S,
144.9348 E and rejoins at 35.6681 S, 145.2437 E.

## The neck rule, generalised

Casino's neck was built from the convex hull of the 5 km disc and the part of the
band within a fixed 8 km window. That constant does not survive Deniliquin, whose
disc edge sits **14.9 km** from the 15 km band — an 8 km window clips nothing and
the hull leaves the disc detached.

The rule is now **window = the gap from the disc to the band + 5 km**, applied to
both. Deniliquin gets a 19.9 km window; Casino's works out at 8.6 km, which moves
its geometric area by 7 km² (6,713 → 6,706 km²) and nothing else.

## Effect

| | Before | After |
|---|---|---|
| Open Area 1 — road-routed | 17,545 km² | **17,993 km²** |
| Open Area 1 — geometric | 17,671 km² | **18,060 km²** |
| Open Area 2 — geometric | 6,713 km² | 6,706 km² *(neck rule only)* |
| Active PMA — road-routed | 763,006 km² | **762,558 km²** |
| Active PMA — geometric | 762,937 km² | **762,539 km²** |

Four localities join Open Area 1: **Deniliquin**, **Deniliquin North** and
**Cornalla** on both versions, and **Tuppal** on the routed version only.

> Unchanged but worth knowing: **Mathoura** has always been `open` on the
> geometric boundary and `active` on the routed one — it sits 8.2 km from the
> border, inside the 15 km line, but the routed boundary runs north of it. That
> predates this work and is not a consequence of it. The handover's "Open Area 1
> (in)" list reflects the geometric version.

## Reproducing it

`scripts/build_oa1_deniliquin.py` reads `data/oa1_deniliquin_route.txt`, splices
it into the routed Open Area 1 boundary to produce
`data/oa1_route_deniliquin.txt`, cuts New South Wales with the result and
rewrites `open_road`, `open_exact` and `line_snap`. It runs **before**
`build_oa2_casino_border.py`, which recomputes the Active PMA and every
locality's zone from whatever the two open areas have become.
