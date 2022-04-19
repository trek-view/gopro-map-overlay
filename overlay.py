# TODO: Resize overlay map to be 10% width of the main video and the height will be resized while keeping its aspect ratio
# idea:
#   1. Use opencv to achieve this
#   2. Scale using ffmpeg

# use ffmpeg-python
import ffmpeg
import os
from os import listdir
from os.path import isfile, join
import json
import sys
import cv2

image_dir = "./images/"
videopath = 'sample.mp4'
outpath = 'out.mp4'
jsonpath = "data.json"

if len(sys.argv) == 5:
    jsonpath = sys.argv[1]
    image_dir = sys.argv[2]
    videopath = sys.argv[3]
    outpath = sys.argv[4]

def create_overlay(geojson):
    global work_dir

    # Get images list from image directory
    image_list = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]
    image_len = len(image_list)

    # Get map image dimension
    geopoints = geojson["1"]["streams"]["GPS5"]["samples"]
    geo_i = 0
    map_overlay = cv2.imread(image_dir+("/%06d"%geo_i)+".png")
    height, width, layers = map_overlay.shape

    # Initialize variables
    fps = geojson['frames/second']
    interval = 1000/fps
    ms = 0
    cur_frame = 0
    frames = 0
    sec = 0

    images = []
    cur_point = geopoints[0]

    print("Building overlay video...")
    print("FPS:", fps, "; Frame interval (ms):",interval)

    while True:
        while cur_point["cts"] < ms:
            geo_i += 1
            if geo_i == image_len:
                break
            cur_point = geopoints[geo_i]
            
        if geo_i == image_len:
            break
            
        filename = ("%06d"%geo_i)+".png"
        images.append(cv2.imread(image_dir+"/"+filename))
        frames += 1
        print("Frame: ", frames, "; Image File: ", filename, "; Timestamp (second)", sec, "; Frame time (ms):", ms, "; Point's cts:", cur_point["cts"])
        
        cur_frame += 1
        ms += interval

        if cur_frame == fps:
            cur_frame = 0
            sec += 1
            ms = sec * 1000

    out = cv2.VideoWriter(work_dir + '/overlay.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))

    for i in range(len(images)):
        out.write(images[i])

    out.release()

# get geojson data
f = open(jsonpath)
geojson = json.load(f)
f.close()

# prepare work directory
work_dir = "./.outfile"
isExist = os.path.exists(work_dir)

if not isExist:
  # Create a new directory because it does not exist 
  os.makedirs(work_dir)

create_overlay(geojson)

# get main video
stream = ffmpeg.input(videopath)
overlay = ffmpeg.input(work_dir+'/overlay.mp4')

stream = ffmpeg.overlay(stream, overlay, x="2*W/100", y="H-h-2*H/100")

stream = ffmpeg.output(stream, outpath)
cmd = ffmpeg.compile(stream)

# get all streams and copy them to output
# retain original video's stream order
# remove video stream from existing command
cmd.remove('-map')
cmd.remove('[s0]')
# probe input video for the streams
streams = ffmpeg.probe(videopath)['streams']
stream_maps = []
# copy streams without messing with the order
for s in streams:
    cmd.insert( len(cmd) - 1, "-map" )
    if s['codec_type'] != 'video':
        cmd.insert( len(cmd) - 1, "0:%d" % s['index'] )
    else:
        cmd.insert( len(cmd) - 1, "[s0]" )

print("======= FFMPEG COMMAND =======")
print(' '.join(cmd))
print("===== FFMPEG COMMAND END =====")

# execute ffmpeg command
os.system(' '.join(cmd))