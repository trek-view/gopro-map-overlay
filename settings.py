VARIABLES = {}
with open('variables.txt', 'r') as f:
    for variable in f.readlines():
        value = variable.split(':')[1].strip()
        if value.isdigit():
            value = int(value)
        key = variable.split(':')[0]
        VARIABLES[key] = value

REQUIRED_VARIABLES = ['mapbox_username', 'mapbox_key', 'mapbox_username']

for var in REQUIRED_VARIABLES:
    if not VARIABLES.get(var):
        raise ValueError(f'Mapbox {var} missing in the variables.txt file.')

if not VARIABLES.get('image_width'):
    VARIABLES['image_width'] = 500
if not VARIABLES.get('image_height'):
    VARIABLES['image_height'] = 300
