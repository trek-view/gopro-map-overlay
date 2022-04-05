import json
from geojson import Point
import os
import argparse

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

def main():
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

		try: 
			os.mkdir(f"./{files_dir}") 
		except OSError as error: 
			print(error)  

		for index, x in enumerate(data):
			f = open(f"./{files_dir}/{index:06}.geojson", "x")

			filedata = f'{{"type": "Point","coordinates": {[x["GPS (Lat.) [deg]"], x["GPS (Long.) [deg]"]]}}}'
			f.write(filedata)
			f.close()

if __name__ == '__main__':
	main()