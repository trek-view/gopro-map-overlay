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
import cv2
import settings
from settings import OVERLAY_OFFSETS, OVERLAY_RATIO
from services import geojson_service
import exiftool
import re
import pathlib

def create_overlay(geojson):
    # Get images list from image directory
    image_list = [f for f in listdir(f"{settings.WORK_DIR}/{geojson_service.images_dir}") if isfile(join(f"{settings.WORK_DIR}/{geojson_service.images_dir}", f))]
    image_len = len(image_list)

    # Get map image dimension
    geopoints = geojson["1"]["streams"]["GPS5"]["samples"]
    geo_i = 0
    map_overlay = cv2.imread(f"{settings.WORK_DIR}/{geojson_service.images_dir}"+("/%06d"%geo_i)+".png")
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
        images.append(cv2.imread(f"{settings.WORK_DIR}/{geojson_service.images_dir}"+"/"+filename))
        frames += 1
        print("Frame: ", frames, "; Image File: ", filename, "; Timestamp (second)", sec, "; Frame time (ms):", ms, "; Point's cts:", cur_point["cts"])
        
        cur_frame += 1
        ms += interval

        if cur_frame == fps:
            cur_frame = 0
            sec += 1
            ms = sec * 1000

    out = cv2.VideoWriter('%s/overlay.avi'%(settings.WORK_DIR),cv2.VideoWriter_fourcc(*'XVID'), fps, (width,height))
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # note the lower case
    # out = cv2.VideoWriter()
    # success = out.open(settings.WORK_DIR + '/overlay.mp4',fourcc,fps,(width,height),True)

    # if success == False:
    #     raise Exception("Cannot open opencv video writer. Exiting...")

    for i in range(len(images)):
        out.write(images[i])

    out.release()

def create(jsonpath, videopath):
    outpath = "%s/%s-overlay.mp4" % (settings.WORK_DIR,pathlib.Path(videopath).stem)

    # get geojson data
    f = open(jsonpath)
    geojson = json.load(f)
    f.close()

    create_overlay(geojson)

    # get main video annd overlay
    stream = ffmpeg.input(videopath)
    overlay = ffmpeg.input('%s/overlay.avi'%(settings.WORK_DIR))
    
    if settings.INPUT_VIDEO_MODE not in OVERLAY_OFFSETS:
        raise ValueError("INPUT_VIDEO_MODE is not supported. Supported modes: 'HERO', '360'.")

    offset_x = settings.VIDEO_OVERLAY_L_OFFSET
    if re.search("px$", str(offset_x)):
        offset_x = offset_x.replace("px", "").strip()
    else:
        offset_x = "%.3f*W" % float(settings.VIDEO_OVERLAY_L_OFFSET)
    
    offset_y = settings.VIDEO_OVERLAY_B_OFFSET
    if re.search("px$", str(offset_y)):
        offset_y = offset_y.replace("px", "").strip()
        offset_y = "H-h-%s" %offset_y
    else:
        offset_y = "H-h-%.3f*H" % float(settings.VIDEO_OVERLAY_B_OFFSET)

    stream = ffmpeg.overlay(stream, overlay, x = offset_x, y = offset_y)

    stream = ffmpeg.output(stream, outpath)
    cmd = ffmpeg.compile(stream)

    # get all streams and copy them to output
    # retain original video's stream order
    # remove video stream from existing command
    cmd.remove('-map')
    cmd.remove('[s0]')
    # probe input video for the streams
    streams = ffmpeg.probe(videopath)['streams']
    # copy streams without messing with the order
    for s in streams:        
        if s['codec_type'] != 'video':
            if 'codec_name' in s:
                cmd.insert( len(cmd) - 1, "-map" )
                cmd.insert( len(cmd) - 1, "0:%d" % s['index'] )
        else:
            cmd.insert( len(cmd) - 1, "-map" )
            cmd.insert( len(cmd) - 1, "[s0]" )

    print("======= FFMPEG COMMAND =======")
    print(' '.join(cmd))
    print("===== FFMPEG COMMAND END =====")

    # execute ffmpeg command
    os.system(' '.join(cmd) + " -y")

    # copy metadata using exiftool
    os.system('exiftool -TagsFromFile %s "-all:all>all:all" %s'%(videopath, outpath))

def set_overlay_dimensions(videopath):
    if settings.INPUT_VIDEO_MODE not in OVERLAY_RATIO:
        raise ValueError("INPUT_VIDEO_MODE is not supported. Supported modes: 'HERO', '360'.")

    streams = ffmpeg.probe(videopath)['streams']
    for s in streams:
        if s['codec_type'] == 'video':
            w = s['width']
            h = s['height']
            
            mode = "HERO"
            
            try:
                # Get 360 tag
                mode = determine_mode(videopath)
            except:
                print("exiftool is not found. Automatic equirectangular video detection is disabled.")

            settings.set_overlay_settings(w,h,mode)
            break
    
    print("Overlay settings mode:", settings.INPUT_VIDEO_MODE)
    print("Set overlay dimension to:",settings.MAPBOX_IMG_W,"x",settings.MAPBOX_IMG_H)
    print("Set overlay offset to:","left:%s"%(settings.VIDEO_OVERLAY_L_OFFSET),"bottom:%s"%(settings.VIDEO_OVERLAY_B_OFFSET))

def determine_mode(videopath):
    # Get 360 tag
    with exiftool.ExifToolAlpha() as et:
        projection_type = et.get_tag(videopath, "XMP-GSpherical:ProjectionType")
        if projection_type == "equirectangular":
            return "360"
    
    # xmp tags might be malformed, get the v4 output of exiftool
    os.system("exiftool -v4 -X %s > %s/metadata.xml" % (videopath, settings.WORK_DIR))
    file = open(f"{settings.WORK_DIR}/metadata.xml", 'r')
    lines = file.readlines()
    xml = ""

    for line in lines:
        linesearch = re.search('(?<=\[)(.+?)(?=\])', line)
        if linesearch:
            xml += linesearch.group(1)

    regex = r"<GSpherical:ProjectionType>(.+?)<\/GSpherical:ProjectionType>"
    match = re.search(regex, xml)
    if match and match.group(1) == "equirectangular":
        return "360"
    
    return "HERO"