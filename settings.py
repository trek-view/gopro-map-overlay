with open("variables.txt", "r") as f:
    for variable in f.readlines():
        value = variable.split(":")[1].strip()
        if value.isdigit():
            value = int(value)
        key = variable.split(":")[0]
        vars()[key.upper()] = value

REQUIRED_VARIABLES = ["mapbox_username", "mapbox_key", "mapbox_username", "input_video_mode"]

for var in REQUIRED_VARIABLES:
    if var.upper() not in vars():
        raise ValueError(f"Mapbox {var} missing in the variables.txt file.")

# Height calculated using 4:3 ratio
if not MAPBOX_IMG_W:
    MAPBOX_IMG_W = 500
MAPBOX_IMG_H = int(MAPBOX_IMG_W * 3 / 4)

MAPBOX_LINE_COLOUR_HEX = str(MAPBOX_LINE_COLOUR_HEX).replace("#", "")
MAPBOX_MARKER_COLOUR_HEX = str(MAPBOX_MARKER_COLOUR_HEX).replace("#", "")
MAPBOX_MARKER_LABEL = str(MAPBOX_MARKER_LABEL).replace(".svg", "")
if not MAPBOX_ZOOM_LEVEL:
    MAPBOX_ZOOM_LEVEL = 17
if not MAPBOX_BASE_STYLE:
    MAPBOX_BASE_STYLE = "mapbox/dark-v10"

# Video mode: HERO or 360
if not INPUT_VIDEO_MODE:
    INPUT_VIDEO_MODE = "HERO"

# FFMPEG overlay's x and y settings to position the overlay based on INPUT_VIDEO_MODE
OVERLAY_OFFSETS = {
    "HERO" : {
        # 2% from left, 2% from bottom
        "x": "2*W/100",
        "y": "H-h-2*H/100"
    },
    "360" : {
        # 10% from left, 10% from bottom
        "x": "10*W/100",
        "y": "H-h-10*H/100"
    },
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
}

def set_overlay_dimensions(w, h):
    global MAPBOX_IMG_H
    global MAPBOX_IMG_W
    MAPBOX_IMG_H = h
    MAPBOX_IMG_W = w