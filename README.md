# mbtilesToPngs
This python program takes .mbtiles files and extracts the images and places them into the correct directory structure `/${z}/${x}/${y}.png` that mimicks OpenStreetMap URI tile structure.
This is to allow for offline use of OpenStreetMaps, and I will be using [Flutter_Map](https://github.com/apptreesoftware/flutter_map) along with my own images for offline maps.

## Where to get .mbtiles?
OpenStreetMap says: Apart from very limited testing purposes, you should not use the tiles supplied by OpenStreetMap.org itself. OpenStreetMap is a volunteer-run non-profit body and cannot supply tiles for large-scale commercial use. Rather, you should use a third party provider that makes tiles from OSM data, or generate your own.

[A Guide to generate your own](https://tilemill-project.github.io/tilemill/docs/guides/osm-bright-mac-quickstart/)

This guide will go through the steps for compiling map data, downloading a specific area, customise the map, then export to mbtile. 

Warning! For Mac, when you install TileMill.app, it currently fails to start. Go into *TileMill* > *Updates Preference* > *check Install* Developer Builds. 

## How to use
Make sure you have python3 install.

`python3 mbtilesToPngs.py -i path_to_mbfiles`

for example, I did:
**python3 sqliteReader.py -i ./OSMBright.mbtiles**


[MBTiles](https://wiki.openstreetmap.org/wiki/MBTiles)
[Tiles](https://wiki.openstreetmap.org/wiki/Tiles)

## License
This project is licensed under the [MIT License](LICENSE.md)

## Acknowledgments
Thank you © OpenStreetMap (and) contributors, ODbL for the data!
Thank you AppTreeSoftware for [Flutter_Map](https://github.com/apptreesoftware/flutter_map)


