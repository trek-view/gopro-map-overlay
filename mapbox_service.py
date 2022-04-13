import json
import os
from email.mime import base
from http import HTTPStatus
from time import sleep
from typing import List, Tuple

import requests
from mapbox import StaticStyle, Tilequery, Uploader

from settings import VARIABLES

service = StaticStyle(access_token=VARIABLES['mapbox_key'])
tilequery = Tilequery(access_token=VARIABLES['mapbox_key'])
upload_service = Uploader(access_token=VARIABLES['mapbox_key'])
BASE_STYLE_ID = 'gopro-map-overlay'
MULTILINE_TILESET_ID = 'gopro-multiline-geojson'
DEFAULT_LAYERS = json.loads(open('./styles/base.json', 'r').read())['layers']
# TODO get any from https://www.mapbox.com/gallery/


def create_base_style():
    if not tileset_exists():
        upload_geojson_as_tileset('multiline.geojson')
    layer = {
        "id": "telemetry",
        "source": "gopro-multiline",
        "source-layer": MULTILINE_TILESET_ID,
        "type": "line",
        "paint": {
            "line-color": "#000000"
        }
    }
    # we get the default layers from saved files, as the API doesn't allow us to use templates as we do in Mapbox Studio
    # more templates should be added, selectable with variables.txt
    # our telemetry layer is added at the end so it is visible above everything else
    DEFAULT_LAYERS.append(layer)
    style_request_body = {
        "version": 8,
        "name": "GoPro Overlay Map",
        "id": BASE_STYLE_ID,
        "metadata": {},
        "sources": {
            "gopro-multiline": {
                "url": f"mapbox://{VARIABLES['mapbox_username']}.{MULTILINE_TILESET_ID}",
                "type": "vector"
            },
            # necessary sources for base layers
            # TODO more will probably be needed for other templates (satellite, for example)
            "mapbox://mapbox.mapbox-traffic-v1": {
                "url": "mapbox://mapbox.mapbox-traffic-v1",
                "type": "vector"
            },
            "composite": {
                "url": "mapbox://mapbox.mapbox-streets-v8,mapbox.mapbox-terrain-v2",
                "type": "vector"
            }
        },
        "layers": DEFAULT_LAYERS
    }
    r = requests.post(
        f'https://api.mapbox.com/styles/v1/{VARIABLES["mapbox_username"]}?access_token={VARIABLES["mapbox_key"]}',
        json=style_request_body,
        headers={'Content-Type': 'application/json'}
    )
    VARIABLES['style'] = r.json()['id']
    return VARIABLES['style']


def upload_geojson_as_tileset(geojson: str) -> str:
    upload_resp = upload_service.upload(geojson, MULTILINE_TILESET_ID)
    # This sends the multiline.geojson data to Mapbox to start a tileset creation process
    while True:
        if upload_resp.status_code != 422:
            break
        print("Uploading geojson...")
        upload_resp = upload_service.upload(geojson, MULTILINE_TILESET_ID)
        sleep(1)
    upload_id = upload_resp.json()['id']
    status_resp = upload_service.status(upload_id).json()
    # We wait until Mapbox finishes processing our file, until status is 'complete'
    while True:
        if status_resp['complete']:
            break
        print("Waiting for Mapbox to process geojson...")
        status_resp = upload_service.status(upload_id).json()
        sleep(3)
    return status_resp


def tileset_exists() -> bool:
    """
    This method just checks if there's an existing tileset with the name we set above. This way,
    we will avoid recreating the tileset again each time the script is run.
    # TODO implement similar method for style creation
    """
    uploads = upload_service.list().json()
    for upload in uploads:
        if upload.get('name') == MULTILINE_TILESET_ID and upload['complete']:
            return True
    return False
