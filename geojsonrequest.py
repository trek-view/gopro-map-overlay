import json
import requests
import urllib.parse
import os

directory = "./files"
# Paste in an access token here
access_token = ""

def main():
	index = 0
	try: 
		os.mkdir("./images")
	except OSError as error: 
		print(error)

	for filename in os.listdir(directory):
		with open(f'{directory}/{index}.geojson') as json_file:
			data = json.load(json_file)
			xcoord = data["coordinates"][0]
			ycoord = data["coordinates"][1]

			encodeddata = urllib.parse.quote(json.dumps(data), safe='')

			r = requests.get(f"https://api.mapbox.com/styles/v1/mitchelbourne/cl1jw3qpv005014q4s04zfzea/static/geojson({encodeddata})/{xcoord}, {ycoord},17/500x300?access_token={access_token}")
			
			if r.status_code == 200:
				with open(f"./images/{index}.png", 'wb') as f:
					f.write(r.content)
					f.close()
			else:
				print("Failed to fetch image with status code: ", r.status_code)
		index += 1

if __name__ == '__main__':
	main()