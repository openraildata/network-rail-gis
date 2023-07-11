#!/usr/bin/bash

if [ ! -d venv ]; then
    echo Set up python3 virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
else
    source venv/bin/activate
fi

if [ ! -s network-model.gpkg ]; then
    echo Create network model GeoPKG
    python3 shp2gpkg.py network-model.gpkg network-model/
fi
if [ ! -s organisational-boundaries.gpkg ]; then
    echo Create organisational boundaries GeoPKG
    python3 shp2gpkg.py organisational-boundaries.gpkg organisational-boundaries/
fi
if [ ! -s esta.gpkg ]; then
    echo Create ESTA GeoPKG
    python3 shp2gpkg.py esta.gpkg esta/
fi

