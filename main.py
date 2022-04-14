import argparse
from time import sleep

from services.geojson_service import generate_images, get_data
from services.mapbox_service import create_base_style
from settings import MAPBOX_USER_STYLE

parser = argparse.ArgumentParser()
files_dir = "geojson-files"

parser.add_argument("-f", "--file", help="Telemetry Filename Including .json")
args = parser.parse_args()

if not args.file:
    print(
        "Please provide the telemetry filename (in base directory) using the -f flag, e.g. python3 main.py -f telemetry.json"
    )
    exit()


images_data = get_data(args.file)
# override style recreation (to reuse one created previously, for example)
if not MAPBOX_USER_STYLE:
    MAPBOX_USER_STYLE = create_base_style()
    # we wait some seconds just to allow the style to be available (sometimes fails for first few images otherwise)
    sleep(5)
# call the image generator method
generate_images(MAPBOX_USER_STYLE, images_data)
