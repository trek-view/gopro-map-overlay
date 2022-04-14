with open("variables.txt", "r") as f:
    for variable in f.readlines():
        value = variable.split(":")[1].strip()
        if value.isdigit():
            value = int(value)
        key = variable.split(":")[0]
        vars()[key.upper()] = value

REQUIRED_VARIABLES = ["mapbox_username", "mapbox_key", "mapbox_username"]

for var in REQUIRED_VARIABLES:
    if not vars()[var.upper()]:
        raise ValueError(f"Mapbox {var} missing in the variables.txt file.")

# Height calculated using 4:3 ratio
if not MAPBOX_IMG_W:
    MAPBOX_IMG_W = 500
MAPBOX_IMG_H = int(MAPBOX_IMG_W * 3 / 4)

if not MAPBOX_BASE_STYLE:
    MAPBOX_BASE_STYLE = "mapbox/dark-v10"
