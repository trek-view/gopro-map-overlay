import json
import requests
import urllib.parse
import os

files_dir = 'geojson-files'
images_dir = 'mapbox-images'
# Paste in an access token here
access_token = ""

def main():
	index = 0
	try: 
		os.mkdir(f"./{images_dir}")
	except OSError as error: 
		print(error)

	for filename in os.listdir(files_dir):
		with open(f'./{files_dir}/{index:06}.geojson') as json_file:
			data = json.load(json_file)
			xcoord = data["coordinates"][0]
			ycoord = data["coordinates"][1]

			encodeddata = urllib.parse.quote(json.dumps(data), safe='')

			r = requests.get(f"https://api.mapbox.com/styles/v1/trekview/cl1nbz22z002614pn626zhm7u/static/geojson({encodeddata})/{xcoord}, {ycoord},17/500x300?access_token={access_token}")
			
			if r.status_code == 200:
				with open(f"./{images_dir}/{index:06}.png", 'wb') as f:
					f.write(r.content)
					f.close()
					print(f"Fetched image: {index}")
			else:
				print("Failed to fetch image with status code: ", r.status_code)
		index += 1

if __name__ == '__main__':
	main()