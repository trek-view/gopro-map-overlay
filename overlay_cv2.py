"""
Simply display the contents of a video using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.

This script will not handle audio and only show video stream with
overlay map. The result will not be saved.
"""

import cv2
import json
import time

def show_video(geojson):
    start = time.time()
    cam = cv2.VideoCapture('sample.mp4')
    geopoints = geojson["1"]["streams"]["GPS5"]["samples"]
    geo_i = 0
    next_time = geopoints[1]["cts"]
    map_overlay = cv2.imread("images/"+str(geo_i)+".png")
    while True:
        ret_val, img = cam.read()

        # resize main video so it will fit on our screen
        scale_percent = 40 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        now = time.time() - start
        if (now * 1000) > next_time:
            geo_i += 1
            next_time = geopoints[geo_i+1]["cts"]
            map_overlay = cv2.imread("images/"+str(geo_i)+".png")
            
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        # overlay image
        x_offset=30
        y_offset=500
        resized[y_offset:y_offset+map_overlay.shape[0], x_offset:x_offset+map_overlay.shape[1]] = map_overlay

        # uncomment to show cts on screen
        # cv2.putText(resized,str(next_time), (0,300), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.imshow('my webcam', resized)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    # read json
    f = open("data.json")
    geojson = json.load(f)
    f.close()
    # print(geojson)
    show_video(geojson)


if __name__ == '__main__':
    main()