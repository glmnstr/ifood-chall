from flask import Flask
from spotAPI import spotifyAPI
from flask import request, jsonify, render_template, flash, make_response, redirect, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import json
from flask_wtf import FlaskForm
from weatherAPI import weather_API
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
import secrets
import string
from urllib.parse import urlencode
import os
from dominate.tags import img
from flask import jsonify

client_id = "a16059247336496a830d64cc548ae852"

client_secret = "3cd7fd4c13fe433b9c16803dd8205a8a"

cl = spotifyAPI(client_id, client_secret)
weather = weather_API()

#url = "http://api.openweathermap.org/data/2.5/weather?q=Porto Alegre&appid="
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["DEBUG"] = True
app.config['SESSION_TYPE'] = 'filesystem'

#app.config.from_object(__name__)

def temp(a):

	if a != None:
		if a > float(30.1):
			return "party"
		elif a in range(15, 30):
			return "pop"
		elif a in range(10, 14):
			return "rock"
		elif a < 9:
			return "classical"

logo = img(src='logo.png', height="50", width="50", style="margin-top:-15px")
topbar = Navbar(logo,
                View('News', 'index'),
                )
REDIRECT_URI = "http://127.0.0.1:5000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"

nav = Nav()
nav.register_element('top', topbar)
Bootstrap(app)

@app.route("/", methods = ['GET', 'POST'])
@app.route("/index")

def index():
	#cidade = request.form.get("cidade")
	print(request.remote_addr)
	e = request.args.get("cidade")
	if (session["tokens"]):
		users = cl.profile(session["tokens"].get("access_token"))

	if e == None:
		e = "londres"
	
	b = temp(int(weather.getWeatherByName(e)[1]))
	return render_template("index.html", user_info = users ,posts = cl.get_recommendations(b), temp = weather.getWeatherByName(e))

@app.route("/", methods = ['GET'])
@app.route("/recommendations")

def recommendations():
	#a = cl.get_recommendations().get("tracks")
	arr = []
	for a in cl.get_recommendations()['tracks']:
		arr.append(a.get("name"))
	return str(arr)

@app.route("/action", methods = ['POST'])
def action():
	r = request.form.get("cidade")
	return render_template("action.html", red = r)

@app.route("/", methods = ['GET'])
@app.route("/auth")
def getAuthorization():
	state = ''.join(
	    secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
	)
	headers = {
	"client_id" : client_id, 
	"response_type" : "code", 
	"redirect_uri" : "http://127.0.0.1:5000/callback", 
	"scope" :"user-read-private"
	}
	endpoint = "https://accounts.spotify.com/authorize"
	res = make_response(redirect(f'{endpoint}/?{urlencode(headers)}'))
	res.set_cookie('spotify_auth_state', state)
	#req = requests.get(f'{endpoint}/?{urlencode(headers)}')
	#print(res.headers)
	#print(req.headers)
	return res

@app.route("/", methods = ['GET'])
@app.route("/callback")

def callback():
	error = request.args.get('error')
	code = request.args.get('code')
	state = request.args.get('state')
	stored_state = request.cookies.get('spotify_auth_state')

	payload = {
	'grant_type': 'authorization_code',
	'code': code,
	'redirect_uri': REDIRECT_URI,
	}
	res = requests.post(TOKEN_URL, auth=(client_id, client_secret), data=payload)
	res_data = res.json()
	#print(res_data)
	if res_data.get('error') or res.status_code != 200:
		app.logger.error(
		'Failed to receive token: %s',
		res_data.get('error', 'No error information received.'),
		)
		abort(res.status_code)

    # Load tokens into session

	session['tokens'] = {
	'access_token': res_data.get('access_token'),
	'refresh_token': res_data.get('refresh_token'),
	}
	return redirect(url_for('me'))

@app.route("/me", methods = ['GET'])

def me():
	token = request.cookies.get("access_token")
	print(session['tokens'])
	return render_template('me.html', data = cl.profile(session['tokens'].get("access_token")))

nav.init_app(app)

if __name__ == '__main__':
	app.run()
