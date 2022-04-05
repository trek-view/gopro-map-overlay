## Python GeoJSON generator from telemetry GPS Coordinates

*built in python 3*

The multiline.geojson file contains the multiline for the entire path in the dataset, and can be uploaded as a layer for a custom style on mapbox. This was done to shorten the URL requests as there is an 8000 character limit. You can create your own mapbox style, the alter the geojsonrequest script and replace the "mitchelbourne/cl1......" with your own style.

Packages used: geojson, json, os, requests, urllib, argparse

1. Paste telemetry data into the data.json file
2. Run the generategeojson python file to create the geojson files from the data set.
3. Open the geojsonrequest and paste in your mapbox api key into the access_key variable
4. Run the geojson request python file, this will generate the images into the images folder.