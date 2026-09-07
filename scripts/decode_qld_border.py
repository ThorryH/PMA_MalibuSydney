"""Decode the OSM NSW/Queensland border polyline into data/qld_border.geojson.

The border is the set of ways shared by the OpenStreetMap admin_level=4
relations for New South Wales and Queensland — the same administrative line
consumer maps render. The sandbox cannot reach the Overpass mirrors, so the
query and the way-chaining are done in a browser page and the result is carried
across as a delta-encoded polyline (Google's encoded-polyline algorithm at 1e-6
precision, on a URL-safe alphabet), simplified to 20 m.
"""
import json, pathlib
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
IX = {c: i for i, c in enumerate(AL)}
ROOT = pathlib.Path(__file__).resolve().parent.parent

def decode(s):
    pts, i, lat, lon = [], 0, 0, 0
    while i < len(s):
        vals = []
        for _ in range(2):
            shift = result = 0
            while True:
                b = IX[s[i]]; i += 1
                result |= (b & 0x1f) << shift; shift += 5
                if b < 0x20: break
            vals.append(~(result >> 1) if result & 1 else (result >> 1))
        lat += vals[0]; lon += vals[1]
        pts.append([round(lon / 1e6, 6), round(lat / 1e6, 6)])
    return pts

enc = (ROOT / 'data/qld_border.enc').read_text().strip()
coords = decode(enc)
json.dump({"type": "Feature", "properties": {
    "id": "qld_border",
    "source": "OpenStreetMap admin_level=4 relations, NSW ∩ QLD shared ways",
    "licence": "ODbL", "simplified_m": 20, "vertices": len(coords)},
    "geometry": {"type": "LineString", "coordinates": coords}},
    open(ROOT / 'data/qld_border.geojson', 'w'))
print(f"{len(coords):,} vertices -> data/qld_border.geojson")
print("  from", coords[0], "to", coords[-1])
