## Python GeoJSON generator from telemetry GPS Coordinates

Use GoPro telemetry to generate a picture-in-picture map.

## Usage

0. Install required packages `pip3 install -r requirements.txt`
1. First extract the telemetry file (as json) from your GoPro video using [gopro-telemetry](https://github.com/JuanIrache/gopro-telemetry/). [Detailed instructions about how to do this can be found in this post](https://www.trekview.org/blog/2022/gopro-telemetry-exporter-getting-started/).
2. Run the `python3 generategeojson.py -f TELEMETRY.json` to create the `.geojson` files from the data set (making sure to replace `TELEMETRY.json` with the telemetry file created at step 1). This will create of sequentially numbered `.geojson` files for each GPS time/lat/lon in the telemetry file in the directory `geojson-files/`.
3. The `multiline.geojson` file generated contains the multiline for the entire path in the dataset, and [should be uploaded as a layer for a custom style on MapBox here](https://studio.mapbox.com/styles).
  * Note: This was done to shorten the URL requests as [there is an 8192 character limit](https://docs.mapbox.com/api/overview/#url-length-limits), therefore the entire `.geojson` file for the `LineString` cannot be passed in a single request.
4. Open the `geojsonrequest.py` and:
  * paste in your MapBox API key into the `access_key` variable. [You can get a MapBox API key here](https://account.mapbox.com/) that will allow you [50,000 free static image lookups each month](https://www.mapbox.com/pricing/#glstatic).
  * paste in your username and layer replacing `USERNAME/STYLE_ID/`. For example `trekview/cl1nbz22z002614pn626zhm7`
5. Run `python3 geojsonrequest.py`. This will generate .jpg map images in the directory `mapbox-images/`.


## Todo 

1. Automate step 3 by creating a mapbox style programatically
2. Add the final logic to overlay mapbox images on video
3. Bundle everything into a single script, taking `variables.txt` and an input json via the command line.

## License

The code of this site is licensed under a [MIT License](/LICENSE).