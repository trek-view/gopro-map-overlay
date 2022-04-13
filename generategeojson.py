import argparse
import json
import os

from geojson import Point

parser = argparse.ArgumentParser()
files_dir = 'geojson-files'

parser.add_argument("-f", "--file", help="Telemetry Filename Including .json")
args = parser.parse_args()

# Find the samples value in dict
def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
            yield value


def generate_multiline_geojson(data):
    multiline = []
    filedata = ''

    for index, x in enumerate(data[1::2]):
        multiline.append([
            [data[index][0], data[index][1]],
            [data[index + 1][0], data[index + 1][1]]
        ])

    filedata = f'{{"type": "FeatureCollection","features": [{{"type": "Feature","geometry": {{"type": "MultiLineString","coordinates": {multiline}}},"properties": {{"prop0": "value0"}}}}]}}'

    f = open(f"./multiline.geojson", "w")
    f.write(filedata)
    f.close()


def get_data():
    if not args.file:
        print("Please provide the telemetry filename (in base directory) using the -f flag, e.g. python3 generategeojson.py -f mytelemetry.json")
        exit()

    with open(f'./{args.file}') as json_file:
        data = json.load(json_file)
        linestring = []

        for x in find_by_key(data, "samples"):
            data = x

        for x in data:
            linestring.append(
                [x['GPS (Lat.) [deg]'], x['GPS (Long.) [deg]']]
            )

        generate_multiline_geojson(linestring)

        return [
            {
                "type": "Point",
                "coordinates": [
                    line[0],
                    line[1],
                ],
            }
            for line in linestring
        ]


if __name__ == '__main__':
    get_data()
