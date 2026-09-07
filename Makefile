PW ?= malsyd

.PHONY: all data geometry map lock clean

all: data geometry map lock

data:
	./scripts/fetch_data.sh

geometry:
	cd work && python3 ../scripts/build_geometry.py && python3 ../scripts/build_towns.py
	cd work && python3 ../scripts/build_overview.py
	cp work/pma.geojson work/towns.json data/
	cp work/pma_state_overview.png assets/state-overview.png
	python3 scripts/build_oa2_south_route.py
	python3 scripts/decode_qld_border.py
	python3 scripts/build_oa1_deniliquin.py
	python3 scripts/build_oa2_casino_border.py

map:
	python3 scripts/build_map.py

lock:
	PMA_PASSWORD=$(PW) python3 scripts/encrypt.py

clean:
	rm -rf work local
