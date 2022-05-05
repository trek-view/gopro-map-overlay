import json
import os
from email.mime import base
from http import HTTPStatus
from time import sleep
from typing import List, Tuple

import requests
from mapbox import Uploader
import settings
from services import geojson_service

upload_service = Uploader(access_token=settings.MAPBOX_KEY)
BASE_STYLE_ID = "gopro-map-overlay"
MULTILINE_TILESET_ID = "gopro-multiline-geojson"


def get_style_layers():
    r = requests.get(
        f"https://api.mapbox.com/styles/v1/{settings.MAPBOX_BASE_STYLE}?access_token={settings.MAPBOX_KEY}"
    )
    if r.status_code != 200:
        return []
    return r.json()["layers"]


def create_base_style():
    upload_geojson_as_tileset(f"{settings.WORK_DIR}/multiline.geojson")
    layer = {
        "id": "telemetry",
        "source": "gopro-multiline",
        "source-layer": MULTILINE_TILESET_ID,
        "type": "line",
        "paint": {
            "line-color": f'#{settings.MAPBOX_LINE_COLOUR_HEX or "000000"}',
            "line-width": settings.MAPBOX_LINE_WIDTH or 1,
        },
    }
    # we get the default layers from saved files, as the API doesn't allow us to use templates as we do in Mapbox Studio
    # more templates should be added, selectable with variables.txt
    # our telemetry layer is added at the end so it is visible above everything else
    DEFAULT_LAYERS = get_style_layers()
    DEFAULT_LAYERS.append(layer)
    style_request_body = {
        "version": 8,
        "name": "GoPro Overlay Map",
        "id": BASE_STYLE_ID,
        "metadata": {},
        "sources": {
            "gopro-multiline": {
                "url": f"mapbox://{settings.MAPBOX_USERNAME}.{MULTILINE_TILESET_ID}",
                "type": "vector",
            },
            # necessary sources for base layers
            # TODO more will probably be needed for other templates (satellite, for example)
            "mapbox://mapbox.mapbox-traffic-v1": {
                "url": "mapbox://mapbox.mapbox-traffic-v1",
                "type": "vector",
            },
            "composite": {
                "url": "mapbox://mapbox.mapbox-streets-v8,mapbox.mapbox-terrain-v2",
                "type": "vector",
            },
        },
        "layers": DEFAULT_LAYERS,
    }
    r = requests.post(
        f"https://api.mapbox.com/styles/v1/{settings.MAPBOX_USERNAME}?access_token={settings.MAPBOX_KEY}",
        json=style_request_body,
        headers={"Content-Type": "application/json"},
    )
    settings.MAPBOX_USER_STYLE = r.json()["id"]
    return settings.MAPBOX_USER_STYLE


def upload_geojson_as_tileset(geojson: str):
    upload_resp = upload_service.upload(geojson, MULTILINE_TILESET_ID)
    # This sends the multiline.geojson data to Mapbox to start a tileset creation process
    while True:
        if upload_resp.status_code != 422:
            break
        print("Uploading geojson...")
        upload_resp = upload_service.upload(geojson, MULTILINE_TILESET_ID)
        sleep(1)
    upload_id = upload_resp.json()["id"]
    status_resp = upload_service.status(upload_id).json()
    # We wait until Mapbox finishes processing our file, until status is 'complete'
    while True:
        if status_resp["complete"]:
            break
        print("Waiting for Mapbox to process geojson...")
        status_resp = upload_service.status(upload_id).json()
        sleep(3)
    return status_resp


def generate_image(coords, style):
    r = requests.get(
        (
            f"https://api.mapbox.com/styles/v1/{settings.MAPBOX_USERNAME}/{style}/"
            f"static/pin-s{f'-{settings.MAPBOX_MARKER_LABEL}' if settings.MAPBOX_MARKER_LABEL else ''}+{settings.MAPBOX_MARKER_COLOUR_HEX or 'ffffff'}({coords[0]},{coords[1]})/{coords[0]}, {coords[1]},{settings.MAPBOX_ZOOM_LEVEL}/"
            f"{settings.MAPBOX_IMG_W}x{settings.MAPBOX_IMG_H}?access_token={settings.MAPBOX_KEY}"
        )
    )
    if r.status_code == 200:
        return r.content
    print("Failed to fetch image with status code: ", r.status_code)
    return None


def tileset_exists():
    """
    This method just checks if there's an existing tileset with the name we set above. This way,
    we will avoid recreating the tileset again each time the script is run.
    # TODO implement similar method for style creation
    """
    uploads = upload_service.list().json()
    if uploads == {"message": "Unauthorized"}:
        raise ValueError(
            "Your Mapbox API Key is not valid. The token must have permissions for Tilesets:Read, Tilesets:List and Tilesets:Write"
        )
    for upload in uploads:
        if upload.get("name") == MULTILINE_TILESET_ID and upload["complete"]:
            return True
    return False
