import json
import os
import urllib.parse
from multiprocessing.sharedctypes import Value

import requests
from settings import MAPBOX_KEY, MAPBOX_USERNAME

from services.mapbox_service import generate_image

files_dir = "geojson-files"
images_dir = "mapbox-images"

def set_working_directory(d):
    global files_dir
    global images_dir
    files_dir = d
    images_dir = os.path.join(d, images_dir)

def generate_images(style, images_data):
    try:
        os.mkdir(f"{images_dir}")
    except OSError as error:
        print(error)

    for index, data in enumerate(images_data):
        image = generate_image(data, style)

        if image:
            with open(f"{images_dir}/{index:06}.png", "wb") as f:
                f.write(image)
                f.close()
                print(f"Fetched image: {index}")


# Find the samples value in dict
def find_by_key(data, target):
    if target in data.keys():
        return data[target]
    for key, value in data.items():
        if isinstance(value, dict):
            return find_by_key(value, target)


def generate_multiline_geojson(data):
    multiline = []
    filedata = ""

    for index, x in enumerate(data[1::2]):
        multiline.append(
            [[data[index][0], data[index][1]], [data[index + 1][0], data[index + 1][1]]]
        )

    filedata = f'{{"type": "FeatureCollection","features": [{{"type": "Feature","geometry": {{"type": "MultiLineString","coordinates": {multiline}}},"properties": {{"prop0": "value0"}}}}]}}'

    f = open(f"{files_dir}/multiline.geojson", "w")
    f.write(filedata)
    f.close()


def get_data(file: str):
    with open(f"{file}") as json_file:
        data = json.load(json_file)
        linestring = []

        data = find_by_key(data, "GPS5").get("samples", [])

        for x in data:
            if "GPS (Lat.) [deg]" in x:
                linestring.append([x["GPS (Lat.) [deg]"], x["GPS (Long.) [deg]"]])
            else:
                linestring.append([x["value"][1], x["value"][0]])

        generate_multiline_geojson(linestring)
        return linestring
