# TODO: Resize overlay map to be 10% width of the main video and the height will be resized while keeping its aspect ratio
# idea:
#   1. Use opencv to achieve this
#   2. Scale using ffmpeg

# use ffmpeg-python
import ffmpeg
from os import listdir
from os.path import isfile, join
import json
import sys

image_dir = "./images/"
videopath = 'sample.mp4'
outpath = 'out.mp4'
jsonpath = "data.json"

if len(sys.argv) == 5:
    jsonpath = sys.argv[1]
    image_dir = sys.argv[2]
    videopath = sys.argv[3]
    outpath = sys.argv[4]

# get image list

image_list = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]
overlays = []

# get geojson data
f = open(jsonpath)
geojson = json.load(f)
f.close()
geopoints = geojson["1"]["streams"]["GPS5"]["samples"]

# get main video
stream = ffmpeg.input(videopath)

x = 0

# load images to overlay
for im in image_list:
    overlays.append(ffmpeg.input(image_dir+im))

for i, geopoint in enumerate(geopoints):
    if(i == len(overlays)):
        break

    time_str = "lt(t,%f)" % (geopoints[i+1]['cts']/1000)
    stream = ffmpeg.overlay(stream, overlays[i], x="2*W/100", y="H-h-2*H/100", enable=time_str)

    if(i == len(geopoints)-2):
        break

stream = ffmpeg.output(stream, outpath)

# WARNING: will throw error if there are too many images on windows (command line argument too long)
ffmpeg.run(stream)

# Workaround Ideas:
# 1. Create frames using opencv and pack it back using ffmpeg, combine with original audio (opencv cannot handle audio)
# 2. Use option --filter_complex_script from ffmpeg to pass filter options, and also use %d on input option to abbreviate the commands.