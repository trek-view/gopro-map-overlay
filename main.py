from time import sleep

from generategeojson import get_data
from geojsonrequest import generate_images
from mapbox_service import create_base_style
from settings import VARIABLES

images_data = get_data()
# override style recreation (to reuse one created previously, for example)
style = VARIABLES.get('style')
if not style:
    style = create_base_style()
    # we wait some seconds just to allow the style to be available (sometimes fails for first few images otherwise)
    sleep(3)
# call the image generator method
generate_images(style, images_data)
