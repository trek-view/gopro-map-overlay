## Python GeoJSON generator from telemetry GPS Coordinates

Use GoPro telemetry to generate a picture-in-picture map.

## Usage

0. Install required packages `pip3 install -r requirements.txt`
1. First extract the telemetry file (as json) from your GoPro video using [gopro-telemetry](https://github.com/JuanIrache/gopro-telemetry/). [Detailed instructions about how to do this can be found in this post](https://www.trekview.org/blog/2022/gopro-telemetry-exporter-getting-started/).
2. Run the `python3 generategeojson.py -f TELEMETRY.json` to create the `.geojson` files from the data set (making sure to replace `TELEMETRY.json` with the telemetry file created at step 1). This will create of sequentially numbered `.geojson` files for each GPS time/lat/lon in the telemetry file in the directory `geojson-files/`.
3. The `multiline.geojson` file generated contains the multiline for the entire path in the dataset, and [should be uploaded as a layer for a custom style on MapBox here](https://studio.mapbox.com/styles).
4. Open the `geojsonrequest.py` and:
  * paste in your MapBox API key into the `access_key` variable. 
  * paste in your username and layer replacing the default `trekview/cl1nbz22z002614pn626zhm7u`.
5. Run `python3 geojsonrequest.py`. This will generate .jpg map images in the directory `mapbox-images/`.
6. Image overlay on video TODO

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
3. Add variables to MapBox Scripts (mapbox_img_w - as shown 
2. Add the final logic to overlay mapbox images on video
3. Bundle everything into a single script, taking `variables.txt` and an input json via the command line.

## Overlay Scripts

There are 2 scripts: overlay.py (ffmpeg) and overlay_cv2.py (opencv)

### overlay.py

This script requires ffmpeg installed in the system and ffmpeg-python, opencv-python from pip. For example, in Ubuntu:

    # install ffmpeg
    sudo apt install ffmpeg

    # install opencv
    pip install opencv-python

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

## License

The code of this site is licensed under a [MIT License](/LICENSE).