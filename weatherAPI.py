import requests
import json
#from teste import spotifyAPI

#git_rec_key = "b77e07f479efe92156376a8b07640ced"
key_weather = "b77e07f479efe92156376a8b07640ced"
#spt_client = "a16059247336496a830d64cc548ae852"

"""
If temperature (celcius) is above 30 degrees, suggest tracks for party
In case temperature is between 15 and 30 degrees, suggest pop music tracks
If it's a bit chilly (between 10 and 14 degrees), suggest rock music tracks
Otherwise, if it's freezing outside, suggests classical music tracks
"""

class weather_API():

	url = "http://api.openweathermap.org/data/2.5/weather?q="
	key = "b77e07f479efe92156376a8b07640ced"

	def getWeatherByName(self, name='Porto Alegre'):
		url = self.url + name + "&appid=" + self.key
		r = requests.get(url)

		data = json.loads(r.text)
		temp = int(data.get('main')['temp']) - 273.15
		return data['name'], temp



#a = weatherAPI()
#print(a.getWeatherByName("Porto Alegre"))