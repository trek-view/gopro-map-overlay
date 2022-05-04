import argparse
from time import sleep

import os
from services.geojson_service import generate_images, get_data
from services.mapbox_service import create_base_style
from settings import MAPBOX_USER_STYLE, set_working_directory
import overlay

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="Telemetry Filename Including .json")
parser.add_argument("-i", "--input", help="Input video file name.")
parser.add_argument("-o", "--output", help="Output directory, if it doesn't exist, it will be created.")
args = parser.parse_args()

if not args.file or not args.input or not args.output:
    parser.print_help()
    exit()

# check if input video exists
if not os.path.isfile(args.input):
    raise Exception("Input video file not found!")

# check output directory, if it is exist as a file, throw an error
if os.path.exists(args.output):
    if os.path.isfile(args.output):
        raise Exception("There is a file with the same name as the specified output directory!")
else:
    os.mkdir(args.output)

# set working directory
set_working_directory(args.output)

overlay.set_overlay_dimensions(args.input)

# images_data = get_data(args.file)
# # override style recreation (to reuse one created previously, for example)
# if not MAPBOX_USER_STYLE:
#     MAPBOX_USER_STYLE = create_base_style()
#     # we wait some seconds just to allow the style to be available (sometimes fails for first few images otherwise)
#     sleep(5)
# # call the image generator method
# generate_images(MAPBOX_USER_STYLE, images_data)

# start creating overlay
overlay.create(args.file, args.input)
