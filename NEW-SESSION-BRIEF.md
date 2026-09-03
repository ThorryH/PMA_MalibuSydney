# Paste-ready brief for a new session

Copy everything below the line into a fresh chat, and attach
`malibu-nsw-pma-github-repo.zip`. That is all the context needed.

---

I'm working on a Primary Market Area (PMA) map for Malibu Boats Australia,
supporting a new dealership in Sydney. The project already exists — the zip I've
attached is the full repo. Read `HANDOVER.md` first, then `docs/METHODOLOGY.md`.

Quick orientation so you don't have to reverse-engineer it:

- The PMA is all of NSW + ACT minus two **Open Areas**. Everything else is the
  **Active PMA** (763,642 km²). Don't use the word "territory".
- **Open Area 1** — within 15 km north of the NSW/VIC border. Road-routed
  17,545 km², geometric 17,670 km².
- **Open Area 2** — coastal strip from Grafton north to the QLD border, 35 km
  inland (Grafton's own distance from the coast). The southern edge is nominally
  29.8073 S but is **routed on roads** from the Grafton area east to the sea at
  Diggers Camp — the straight line is kept only as the geometric version.
  Road-routed 6,526 km², geometric 6,545 km². The whole of Grafton is inside;
  there is no separate ring-fence.
- Every boundary has a **road-routed** version and a **geometric** version. The
  road-routed one is operative and shown by default.

How the road routing works: sample the geometric line every 4 km, snap anchors to
the nearest OpenStreetMap road node, join consecutive anchors with **Dijkstra
shortest paths along road centrelines**. Where no connected road network exists
within 12 km, the boundary keeps the geometric line rather than being dragged
off-corridor. Anchor spacing matters — too wide and the route shortcuts through
towns.

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
Casino and Kyogle belong in Open Area 2; whether Deniliquin should be outside
Open Area 1 now that it's 15 km; which boundary version is contractual; and
whether the southern edge of Open Area 2 should keep following the road network
or be redrawn on a single feature (the Clarence River, an LGA boundary, one
named road).

Known gap: the Jindabyne → Cape Howe section of Open Area 1 was never road-routed
because the Overpass mirrors kept timing out. The code works, it just needs the
data through.
