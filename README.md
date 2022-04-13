## Python GeoJSON generator from telemetry GPS Coordinates

Use GoPro telemetry to generate a picture-in-picture map.

## Usage

0. Install required packages `pip3 install -r requirements.txt`
1. First extract the telemetry file (as json) from your GoPro video using [gopro-telemetry](https://github.com/JuanIrache/gopro-telemetry/). [Detailed instructions about how to do this can be found in this post](https://www.trekview.org/blog/2022/gopro-telemetry-exporter-getting-started/).
2. Fill in the `variables.txt` with your Mapbox API Key and username, and other variables if needed.
3. Run `python3 main.py -f TELEMETRY.json`. This will generate a `multiline.geojson` file, upload it to a new style in your Mapbox accountg and generate .jpg map images in the directory `mapbox-images/`.
4. Image overlay on video TODO

## Variable

TODO

To run the script you need to set the following variables:

* `mapbox_key`: your MapBox API key. [You can get a MapBox API key here](https://account.mapbox.com/) that will allow you [50,000 free static image lookups each month](https://www.mapbox.com/pricing/#glstatic).
* `mapbox_base_style`: [Set your basemap style](https://studio.mapbox.com/styles). Options are: `streets`, `outdoors`, `satellite`, `satellite_streets`, `light`, `dark`
* `mapbox_img_w`: defines the width of the image for overlay. Recommended is 20% of video input width. Image height will be generated automatically based of 4:3 resolution.
* `mapbox_zoom_level`: the zoom level for the map (recommended between 8-10). [See MapBox docs for more](https://docs.mapbox.com/help/glossary/zoom-level/).
* `mapbox_marker_colour_hex`: the colour you want for the map point, passed as a 6 digit hex code (e.g. `000000` for black)
* `mapbox_line_colour_hex`: the colour you want for the line passed as a 6 digit hex code
* `video_overlay_l_offset`: Left pixel padding
* `video_overlay_t_offset`:



## Todo 

1. Automate step 3 by creating a mapbox style programatically
2. Merge step 2 and 3 into a single command
3. Add variables to MapBox Scripts
4. Add the final logic to overlay mapbox images on video (to not be done yet)
5. Bundle everything into a single script, taking `variables.txt` and an input json via the command line.

## Overlay Scripts

There are 2 scripts: overlay.py (ffmpeg) and overlay_cv2.py (opencv)

### overlay.py

This script requires ffmpeg installed in the system and ffmpeg-python from pip. For example, in Ubuntu:

    # install ffmpeg
    sudo apt install ffmpeg

    # install ffmpeg-python (assuming it is python 3, or use pip3)
    pip install ffmpeg-python

To run this script:

    python overlay.py [json] [image_directory] [main_video] [output_video_path]

not supplying any of the arguments will result in default value for all arguments.

Default values:

    json = "data.json"
    image_directory = './images/'
    main_video = 'sample.mp4'
    output_video_path = 'out.mp4'

### overlay_cv2.py

This script requires opencv. To install it, run:

    pip install opencv-python

To run this script:

    python overlay_cv2.py [json] [image_directory] [main_video]

not supplying any of the arguments will result in default value for all arguments.

Default values:

    json = "data.json"
    image_directory = './images/'
    main_video = 'sample.mp4'

## License

The code of this site is licensed under a [MIT License](/LICENSE).