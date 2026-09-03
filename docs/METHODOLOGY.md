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
