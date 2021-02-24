from flask import Flask
from teste import spotifyAPI
from flask import request, jsonify
import requests
import json

key_weather = "b77e07f479efe92156376a8b07640ced"
client_id = "a16059247336496a830d64cc548ae852"
client_secret = "3cd7fd4c13fe433b9c16803dd8205a8a"

cl = spotifyAPI(client_id, client_secret)

url = "http://api.openweathermap.org/data/2.5/weather?q=Porto Alegre&appid="

r = requests.get(url + key_weather)
data = json.loads(r.text)

temp = int(data.get('main')['temp']) - 273.15

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods = ['GET'])
@app.route("/index")

def index():

	if int(temp) > 31:
		
		for a in cl.get_recommendations("party")['tracks']:
			for b in a['album']['artists']:
				print (a.get("name")," 	||  ", b.get("name"))
			return "Party ! " + a.get("name") + b.get("name") + str(temp)
		return "teste"

	elif int(temp) in range(15, 31):
		for a in cl.get_recommendations("pop")['tracks']:
			for b in a['album']['artists']:
				print (a.get("name")," 	||  ", b.get("name"))
			return "Pop ! " + a.get("name") + " - - - " + b.get("name") + str(temp)

	elif int(temp) in range(10, 14):

		for a in cl.get_recommendations("rock")['tracks']:
			for b in a['album']['artists']:
				print (a.get("name")," 	||  ", b.get("name"))
			return "Rock ! " + a.get("name") + " - - - " + b.get("name") + str(temp)
		return "ROCK!" + str(temp)
	else:
		for a in cl.get_recommendations("classical")['tracks']:
			for b in a['album']['artists']:
				print (a.get("name")," 	||  ", b.get("name"))
			return "Classic ! " + a.get("name") + " - - - " + b.get("name") + str(temp)
		return "CLASSIC!" + str(temp)
    #return cl.get_categories("BR", "50")

@app.route("/", methods = ['GET'])
@app.route("/recommendations")

def recommendations():
	#a = cl.get_recommendations().get("tracks")
	arr = []
	for a in cl.get_recommendations()['tracks']:
		arr.append(a.get("name"))
	return str(arr)

app.run()
