#!/usr/bin/bash

if [ ! -d venv ]; then
    echo Set up python3 virtual environment
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

if [ ! -s network-model.gpkg ]; then
    echo Create network model GeoPKG
    python shp2gpkg.py network-model.gpkg network-model/
fi
if [ ! -s organisational-boundaries.gpkg ]; then
    echo Create organisational boundaries GeoPKG
    python shp2gpkg.py organisational-boundaries.gpkg organisational-boundaries/
fi

