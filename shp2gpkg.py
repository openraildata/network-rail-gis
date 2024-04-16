#!/usr/bin/env python
# coding: utf-8
"""Grovel directories containing ESRI ShapeFile to create GeoPackage layers"""

import argparse
import os
import re
from os import walk
from pathlib import Path

import pandas as pd
from pyogrio import read_dataframe, write_dataframe

pd.set_option("display.max_columns", None)

PARSER = argparse.ArgumentParser(
    description="Create ESRI shp data as layers in a GeoPackage file"
)
PARSER.add_argument(
    "--output", type=str, default="geo-model.gpkg", nargs="?", help="output filename"
)
PARSER.add_argument("--search", type=str, default=".", nargs="?", help="search path")
PARSER.add_argument(
    "--crs",
    type=str,
    default="EPSG:32630",
    nargs="?",
    help="coordinate reference system",
)

ARGS, REST = PARSER.parse_known_intermixed_args()
REST = (REST + [None] * 3)[:3]
OUTPATH, FILEPATH, CRS = [(i or j) for i, j in zip(REST, vars(ARGS).values())]


def list_files(filepath, match):
    """find all filenames containing match in directories under filepath"""
    files = ()
    for d, _, filenames in walk(filepath):
        if "geopandas/datasets" in d:
            continue
        files = files + tuple(f"{d}/{f}" for f in filenames if match in f)
    return files


PATTERNS = [re.compile(i, re.IGNORECASE) for i in ["shapefile", "shape$", "file$"]]


def get_layername(filepath):
    """return layer name from shape-filepath"""
    r = Path(filepath)
    return r.parent.stem


FILES = [f for f in list_files(FILEPATH, "shp") if f[-4:] == ".shp"]


for f in FILES:
    gf = read_dataframe(f)
    layername = get_layername(f)
    print(f"layer: {layername}")
    write_dataframe(gf.to_crs(CRS), OUTPATH, layer=layername)
