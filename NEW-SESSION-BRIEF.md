# Paste-ready brief for a new session

Copy everything below the line into a fresh chat, and attach
`malibu-nsw-pma-github-repo.zip`. That is all the context needed.

---

I'm working on a Primary Market Area (PMA) map for Malibu Boats Australia,
supporting a new dealership in Sydney. The project already exists — the zip I've
attached is the full repo. Read `HANDOVER.md` first, then `docs/METHODOLOGY.md`.

Quick orientation so you don't have to reverse-engineer it:

- The PMA is all of NSW + ACT minus two **Open Areas**. Everything else is the
  **Active PMA** (762,536 km²). Don't use the word "territory".
- **Open Area 2 meets the NSW/QLD border; the Active PMA is held 500 m south of
  it.** Neither crosses, and ~410 km² of NSW is consequently in no zone along the
  Active PMA's stretch — that is deliberate. Open Area 2's northern limit is the
  OSM line itself, not the state outline, which falls up to 300 m short of it. That border is the
  OpenStreetMap `admin_level=4` line (4,845 vertices, 1,681 km) in
  `data/qld_border.geojson`, **not** the 1:250k `states.geojson` outline the rest of
  the build uses — the old one ran a median 109 m from the real border. Nothing
  touches or crosses the state line; checked at 1 km intervals along the whole
  length. The Victorian border is still 1:250k.
- **Open Area 1** — within 15 km north of the NSW/VIC border, **plus Deniliquin**
  (34.9 km out) behind a 5 km road-routed boundary. Road-routed 17,993 km²,
  geometric 18,060 km². Deniliquin has **no orbital road** — its roads are
  dead-end radials, so with the town core excluded from the graph there is no
  connected path at all around the west and north, at any radius. Five of eleven
  legs there hold a true 5 km circular arc instead of a road. Don't "fix" it.
- **Open Area 2** — coastal strip from Grafton north to the QLD border, 35 km
  inland (Grafton's own distance from the coast). The southern edge is nominally
  29.8073 S but is **routed on roads** from the Grafton area east to the sea at
  Diggers Camp — the straight line is kept only as the geometric version.
  Road-routed 6,776 km², geometric 6,729 km². **Casino is inside** — it is 43.6 km
  from the coast, so the western boundary detours around it at 5 km and rejoins
  the corridor north and south, as one continuous area. Kyogle is still outside.
  The whole of Grafton is inside too. There is no separate ring-fence for either.
- Every boundary has a **road-routed** version and a **geometric** version. The
  road-routed one is operative and shown by default.

How the road routing works: sample the geometric line every 4 km, snap anchors to
the nearest OpenStreetMap road node, join consecutive anchors with **Dijkstra
shortest paths along road centrelines**. Where no connected road network exists
within 12 km, the boundary keeps the geometric line rather than being dragged
off-corridor. Anchor spacing matters — too wide and the route shortcuts through
towns. Where the boundary has to go *around* a town rather than past it (Casino,
Deniliquin), delete every road node within ~4 km of the town centre from the graph
first, or the shortest paths cut straight back through it — and be ready for the
answer that no ring road exists, in which case hold the true circular arc.

The neck joining an out-of-area town to the main strip is the convex hull of the
5 km disc and the part of the band within (gap to the band + 5 km) of it.

Getting OSM data: the sandbox can't reach Overpass — the egress proxy refuses
every mirror. The working method is to open `https://overpass.kumi.systems/` in a
browser pane and `fetch()` the query from inside that page (same origin, so no
CORS problem), then build the graph and run the Dijkstra routing in the page and
return only the resulting polyline. A large corridor query takes 40–60 s, so kick
it off, stash the promise on `window`, and poll — a single blocking call will time
the tool out. Mirrors `overpass.kumi.systems` and `overpass.private.coffee` both
work but rate-limit; wait 60–120 s between large queries.

Build: `pip install -r scripts/requirements.txt` then `make`. Steps are
`make data | geometry | map | lock PW=malsyd`.

The map is `index.html` — a single self-contained file, MapLibre GL JS with
OpenFreeMap vector tiles, no API key, AES-256 password gate (password `malsyd`).
Do not reintroduce a keyed base map provider.

Things still undecided that you should ask about rather than assume: whether
Kyogle belongs in Open Area 2 (Casino is settled — it's in); which boundary
version is contractual; and
whether the southern edge of Open Area 2 should keep following the road network
or be redrawn on a single feature (the Clarence River, an LGA boundary, one
named road).

Known gap: the Jindabyne → Cape Howe section of Open Area 1 was never road-routed
because the Overpass mirrors kept timing out. The code works, it just needs the
data through.
