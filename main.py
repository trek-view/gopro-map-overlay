import argparse
from time import sleep

from services.geojson_service import generate_images, get_data
from services.mapbox_service import create_base_style
from settings import MAPBOX_USER_STYLE
import overlay

parser = argparse.ArgumentParser()
files_dir = "geojson-files"

parser.add_argument("-f", "--file", help="Telemetry Filename Including .json")
parser.add_argument("-i", "--input", help="Input video file name")
parser.add_argument("-o", "--output", help="Output video file name")
args = parser.parse_args()

if not args.file or not args.input or not args.output:
    parser.print_help()
    exit()
    
overlay.set_overlay_dimensions(args.input)

images_data = get_data(args.file)
# override style recreation (to reuse one created previously, for example)
if not MAPBOX_USER_STYLE:
    MAPBOX_USER_STYLE = create_base_style()
    # we wait some seconds just to allow the style to be available (sometimes fails for first few images otherwise)
    sleep(5)
# call the image generator method
generate_images(MAPBOX_USER_STYLE, images_data)

# start creating overlay
overlay.create(args.file, args.input, args.output)
