## Python GeoJSON generator from telemetry GPS Coordinates

Use GoPro telemetry to generate a picture-in-picture map.

## Prerequisites

1. First extract the telemetry file (as json) from your GoPro video using [gopro-telemetry](https://github.com/JuanIrache/gopro-telemetry/). [Detailed instructions about how to do this can be found in this post](https://www.trekview.org/blog/2022/gopro-telemetry-exporter-getting-started/).
2. Install required packages `pip3 install -r requirements.txt`
3. Fill in the `variables.txt` with your Mapbox API Key and username, and other variables if needed (see `variables.txt` section on this page.

## Usage

`python3 main.py -f TELEMETRY.json -i INPUT.mp4 -o OUT_DIRECTORY`

* `-f`: input telemetry json file (see prerequisites)
* `-i`: input video file you generated telemetry json from (and map should be overlaid on)
* `-o`: output directory for final video file with overlay

### Example usage

```
python3 main.py -f GX010044-gps-only.json -i GX010044.MP4 -o video-overlay/
```

### `variables.txt`

To run the script you need to set the required variables (and optional variables if you don't want to use defaults):

* `mapbox_key` (required): your MapBox API key. [You can get a MapBox API key here](https://account.mapbox.com/) that will allow you [50,000 free static image lookups each month](https://www.mapbox.com/pricing/#glstatic). Ensure your key has the following permissions when you create it; `Styles:Tiles`, `Styles:Read`, `Styles:Write`, `Styles:List`, `Styles:Download`, `Styles:Protect`, `Fonts:Read`, `Datasets:Read`, `Vision:Read`, `Uploads:Read`, `Uploads:List`, `Uploads:Write`, `Tilesets:Read`, `Tilesets:List` and `Tilesets:Write`
    * Default: ''
* `mapbox_username` (required): you MapBox username/account name. [You can see this under your account settings in MapBox](https://account.mapbox.com/)
    * Default: ''
* `mapbox_base_style`: [Set your basemap style](https://docs.mapbox.com/api/maps/styles/). Options include (but not limited to): `mapbox/streets-v11`, `mapbox/outdoors-v11`, `mapbox/satellite-v9`, and `mapbox/satellite-streets-v11`
    * Default: `mapbox/outdoors-v11`
* `mapbox_user_style`: If you want to reuse a previous style you can pass it here like so `trekview/cl20cn42p009i15o97k316e8u` (this variable is not needed 99% of the time).
    * Default: ''
* `mapbox_marker_label`: You can add a label inside the marker. It can be a digit (0-9), a letter (a-z) or a Maki icon (without svg extension, i.e: circle). [List of available icons](https://labs.mapbox.com/maki-icons/).
    * Default: ''
* `mapbox_img_w`: defines the width of the image for overlay as a ratio of input video. 
        * `0.2` (20%) of input video width (for HERO)
        * `0.1` (10%) of input video width (for equirectangular)
* `mapbox_img_h`: defines the height of the image for overlay as a ratio of input video. 
        * `0.2` (20%) of input video width (for HERO)
        * `0.1` (10%) of input video width (for equirectangular)
* `mapbox_zoom_level`: the zoom level for the map (recommended between 8-10). [See MapBox docs for more](https://docs.mapbox.com/help/glossary/zoom-level/). Between 0 and 22. In short, the higher the zoom number, the closer to the ground the zoom is.
    * Default: `10`
* `mapbox_line_colour_hex`: the colour you want for the line passed as a 6 digit hex code
        * Default: #`E48241`
* `mapbox_marker_colour_hex`: the colour you want for the map point, passed as a 6 digit hex code (e.g. `000000` for black)
    * Default: #`000000`
* `mapbox_line_width`: the width in pixels for the linestring.
      * Default: `1`px  
* `video_overlay_b_offset`: defines the bottom offset of the image for overlay as a ratio of input video. Could be set manually to ratio value or px value (20px means 20 pixels off from bottom).
    * Default:
        * `0.02` (2%) video height (for HERO)
        * `0.3` (30%) video height (for equirectangular)
* `video_overlay_l_offset`: defines the left offset of the image for overlay as a ratio of input video. Could be set manually to ratio value or px value (20px means 20 pixels off from left).
    * Default:
        * `0.02` (2%) video width (for HERO)
        * `0.3` (30%) video height (for equirectangular)

#### Sample varible for common GoPro video sizes

##### HERO video

An example `variables.txt` with some custom values;

```
mapbox_key: YOUR_KEY
mapbox_username: YOUR_USER
mapbox_base_style: mapbox/outdoors-v11
mapbox_user_style: 
mapbox_marker_label: circle
mapbox_zoom_level: 15
mapbox_line_colour_hex: ffffff
mapbox_marker_colour_hex: 3bb2d0
mapbox_line_width: 1
mapbox_img_w: 0.2
mapbox_img_h: 0.2
video_overlay_b_offset: 0.02
video_overlay_l_offset: 0.02
```

##### 360 video

An example `variables.txt` with some custom values;

```
mapbox_key: YOUR_KEY
mapbox_username: YOUR_USER
mapbox_base_style: mapbox/outdoors-v11
mapbox_user_style: 
mapbox_marker_label: circle
mapbox_zoom_level: 15
mapbox_line_colour_hex: ffffff
mapbox_marker_colour_hex: 3bb2d0
mapbox_line_width: 1
mapbox_img_w: 0.1
mapbox_img_h: 0.1
video_overlay_b_offset: 0.3
video_overlay_l_offset: 0.3
```

## How it works

1. Script detects if video is equirectangular or normal hero video using exiftool 
2. a `multiline.geojson` file from all .json telemetry points
3. the `multiline.geojson` file is uploaded as a new style to the specified MapBox account
4. the script used the new style which is used to generate a .jpg map images for each point in the `mapbox-images/` directory.
5. The resulting images are wrapped up into a video containing map images at frame spacing rate defined in the telemetry json.
6. The map video is overlaid using ffmpeg to the original video (based on default values or `variables.txt` values) and all streams copied from original video (e.g. video, sound, and telemetry) to the new final video
7. exiftool is used to copy global metadata to the new final video

## License

The code of this site is licensed under a [MIT License](/LICENSE).