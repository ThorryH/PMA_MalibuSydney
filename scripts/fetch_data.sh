#!/usr/bin/env bash
# Downloads the open source datasets the build depends on into ./work
set -euo pipefail
mkdir -p work && cd work

echo "→ Australian state boundaries"
curl -sSL -o states.geojson \
  https://raw.githubusercontent.com/rowanhogan/australian-states/master/states.geojson

echo "→ Natural Earth 10m roads (48 MB)"
curl -sSL -o ne_roads.geojson \
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_roads.geojson

echo "→ Australian localities + coordinates"
curl -sSL -o auspost.csv \
  https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.csv

echo "→ MapLibre GL JS 4.7.1 (inlined into the map)"
curl -sSL -o maplibre-gl.js  https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js
curl -sSL -o maplibre-gl.css https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css

echo "Done."
