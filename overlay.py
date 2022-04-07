# TODO: Resize overlay map to be 10% width of the main video and the height will be resized while keeping its aspect ratio
# idea:
#   1. Use opencv to achieve this
#   2. Scale using ffmpeg

# use ffmpeg-python
import ffmpeg
from os import listdir
from os.path import isfile, join
import json

# get image list
image_path = "./images/"
image_list = [f for f in listdir(image_path) if isfile(join(image_path, f))]
overlays = []

# get geojson data
f = open("data.json")
geojson = json.load(f)
f.close()
geopoints = geojson["1"]["streams"]["GPS5"]["samples"]

# get main video
stream = ffmpeg.input('sample.mp4')

x = 0

# load images to overlay
for im in image_list:
    overlays.append(ffmpeg.input(image_path+im))

for i, geopoint in enumerate(geopoints):
    if(i == len(overlays)):
        break

    time_str = "lt(t,%f)" % (geopoints[i+1]['cts']/1000)
    stream = ffmpeg.overlay(stream, overlays[i], x="2*W/100", y="H-h-2*H/100", enable=time_str)

    if(i == len(geopoints)-2):
        break

stream = ffmpeg.output(stream, 'out.mp4')

# WARNING: will throw error if there are too many images on windows (command line argument too long)
ffmpeg.run(stream)

# Workaround Ideas:
# 1. Create frames using opencv and pack it back using ffmpeg, combine with original audio (opencv cannot handle audio)
# 2. Use option --filter_complex_script from ffmpeg to pass filter options, and also use %d on input option to abbreviate the commands.