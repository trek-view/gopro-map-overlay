import json
import os
import urllib.parse
from multiprocessing.sharedctypes import Value

import requests

from settings import VARIABLES

files_dir = 'geojson-files'
images_dir = 'mapbox-images'
access_token = VARIABLES.get('mapbox_key')
mapbox_username = VARIABLES.get('mapbox_username')


def generate_images(style, images_data):
    try:
        os.mkdir(f"./{images_dir}")
    except OSError as error:
        print(error)

    for index, data in enumerate(images_data):
        xcoord = data["coordinates"][0]
        ycoord = data["coordinates"][1]

        encodeddata = urllib.parse.quote(json.dumps(data), safe='')

        r = requests.get((
            f"https://api.mapbox.com/styles/v1/{mapbox_username}/{style}/"
            f"static/geojson({encodeddata})/{xcoord}, {ycoord},17/"
            f"500x300?access_token={access_token}"
        ))
        if r.status_code == 200:
            with open(f"./{images_dir}/{index:06}.png", 'wb') as f:
                f.write(r.content)
                f.close()
                print(f"Fetched image: {index}")
        else:
            print("Failed to fetch image with status code: ", r.status_code)


if __name__ == '__main__':
    generate_images()
