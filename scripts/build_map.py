"""Inline MapLibre GL JS + the computed GeoJSON into a single self-contained map."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT / "work"

tpl = (HERE / "template.html").read_text()
tpl = tpl.replace("__MLCSS__", (WORK / "maplibre-gl.css").read_text())
tpl = tpl.replace("__MLJS__",  (WORK / "maplibre-gl.js").read_text())
tpl = tpl.replace("__PMA__", json.dumps(
    json.loads((ROOT / "data/pma.geojson").read_text()), separators=(",", ":")))
tpl = tpl.replace("__TOWNS__", json.dumps(
    [{k: (round(v, 4) if k in ("lon", "lat") else v)
      for k, v in t.items() if k != "zr"}
     for t in json.loads((ROOT / "data/towns.json").read_text())], separators=(",", ":")))

out = ROOT / "local" / "map-unlocked.html"
out.parent.mkdir(exist_ok=True)
out.write_text(tpl)
print(f"{out} — {len(tpl)/1024:.0f} KB")
