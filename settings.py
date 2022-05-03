import os

with open("variables.txt", "r") as f:
    for variable in f.readlines():
        value = variable.split(":")[1].strip()
        if value.isdigit():
            value = int(value)
        key = variable.split(":")[0]
        vars()[key.upper()] = value

REQUIRED_VARIABLES = ["mapbox_username", "mapbox_key", "mapbox_username"]

for var in REQUIRED_VARIABLES:
    if var.upper() not in vars():
        raise ValueError(f"Mapbox {var} missing in the variables.txt file.")

MAPBOX_LINE_COLOUR_HEX = str(MAPBOX_LINE_COLOUR_HEX).replace("#", "")
MAPBOX_MARKER_COLOUR_HEX = str(MAPBOX_MARKER_COLOUR_HEX).replace("#", "")
MAPBOX_MARKER_LABEL = str(MAPBOX_MARKER_LABEL).replace(".svg", "")
if not MAPBOX_ZOOM_LEVEL:
    MAPBOX_ZOOM_LEVEL = 17
if not MAPBOX_BASE_STYLE:
    MAPBOX_BASE_STYLE = "mapbox/dark-v10"

if "INPUT_VIDEO_MODE" not in vars():
    INPUT_VIDEO_MODE = "CUSTOM"

# x and y offset (ratio to width and height)
OVERLAY_OFFSETS = {
    "HERO" : {
        # 2% from left, 2% from bottom
        "x": 0.02,
        "y": 0.02
    },
    "360" : {
        # 30% from left, 30% from bottom
        "x": 0.3,
        "y": 0.3
    },
    "CUSTOM" : {
        "x": VIDEO_OVERLAY_L_OFFSET,
        "y": VIDEO_OVERLAY_B_OFFSET
    }
}

# mapbox overlay's dimension setting with ratio to input video's dimensions
OVERLAY_RATIO = {
    "HERO" : {
        # 20% video width, 20% video height
        "w": 0.2,
        "h": 0.2
    },
    "360" : {
        # 10% video width, 10% video height
        "w": 0.1,
        "h": 0.1
    },
    "CUSTOM" : {
        "w": MAPBOX_IMG_W,
        "h": MAPBOX_IMG_H
    }
}

WORK_DIR = ""

def set_overlay_settings(video_w, video_h, mode):
    global MAPBOX_IMG_H
    global MAPBOX_IMG_W
    global INPUT_VIDEO_MODE

    if not MAPBOX_IMG_H:
        INPUT_VIDEO_MODE = mode
        MAPBOX_IMG_H = round(video_h * OVERLAY_RATIO[mode]['h'])
        MAPBOX_IMG_W = round(video_w * OVERLAY_RATIO[mode]['w'])
    else:
        MAPBOX_IMG_H = round(video_h * float(OVERLAY_RATIO[mode]['h']))
        MAPBOX_IMG_W = round(video_w * float(OVERLAY_RATIO[mode]['w']))
    
    if MAPBOX_IMG_H > 1280 or MAPBOX_IMG_H < 1 or MAPBOX_IMG_W > 1280 or MAPBOX_IMG_W < 1:
        raise ValueError("MAPBOX_IMG_H and MAPBOX_IMG_W must be a number between 1 and 1280")

def set_working_directory(wd):
    global WORK_DIR
    isExist = os.path.exists(wd)

    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(wd)
        
    WORK_DIR = wd