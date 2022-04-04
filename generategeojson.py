import json
from geojson import Point
import os

# Find the samples value in dict
def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
        	yield value

def main():
	with open('./data.json') as json_file:
		data = json.load(json_file)
		linestring = []

		for x in find_by_key(data, "samples"):
			data = x

		for x in data:
			linestring.append(
				[x['GPS (Lat.) [deg]'], x['GPS (Long.) [deg]']]
			)

		try: 
			os.mkdir("./files") 
		except OSError as error: 
			print(error)  

		for index, x in enumerate(data):
			f = open(f"./files/{index}.geojson", "x")

			filedata = f'{{"type": "Point","coordinates": {[x["GPS (Lat.) [deg]"], x["GPS (Long.) [deg]"]]}}}'
			f.write(filedata)
			f.close()

if __name__ == '__main__':
	main()