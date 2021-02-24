import requests
import json
import base64
import datetime
from urllib.parse import urlencode

class spotifyAPI(object):
	access_token = None
	access_token_expires = datetime.datetime.now()
	access_did_expires = True
	client_id = None
	client_secret = None
	token_url = "https://accounts.spotify.com/api/token"

	def __init__(self, client_id, client_secret, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client_id = client_id
		self.client_secret = client_secret

	def get_client_credentials(self):
		"""
		returns a base64 encoded string
		"""
		client_id = self.client_id
		client_secret = self.client_secret
		if client_secret == None or client_id == None:
			raise Exception("You must set client_id and client_secret")

		client_creds = f"{client_id}:{client_secret}"
		client_creds_b64 = base64.b64encode(client_creds.encode())

		return client_creds_b64.decode()
	def get_token_header(self):
		client_creds_b64 = self.get_client_credentials()
		return {
				"Authorization" : f"Basic {client_creds_b64}"
		}

	def get_token_data(self):
		return{
		"grant_type" : "client_credentials"
		}

	def perform_auth(self):
		url = self.token_url
		token_data = self.get_token_data()
		token_headers = self.get_token_header()

		r = requests.post(url, data=token_data, headers = token_headers)
		if r.status_code not in range(200 , 299):
			raise Exception("Could not authenticate client.")
		data = r.json()
		now = datetime.datetime.now()
		access_token = data["access_token"]
		expires_in = data["expires_in"]
		expires = now + datetime.timedelta(seconds=expires_in)
		self.access_token = access_token
		self.access_token_expires = expires
		self.access_did_expires = expires < now
		return True

	def get_access_token(self):
		token = self.access_token
		expires = self.access_token_expires
		now = datetime.datetime.now()
		if expires < now:
			self.perform_auth()
			return self.get_access_token()
		elif token == None:
			return self.get_access_token()
		return token

	def get_resource_headers(self):
		access_token = self.get_access_token()
		headers = {
			"Authorization" : f"Bearer {access_token}"
		}
		return headers

	def get_resource(self, loockup_id, resource_type = "albums", version = 'v1' ):
		endpoint = f"https://api.spotify.com/{version}/{resource_type}/{loockup_id}"
		headers = self.get_resource_header()

		r = requests.get(endpoint, headers = headers)
		if r.status_code not in range (200 , 299):
			return {}
		return r.json

	"""

	Uso : get_categories("BR", "50")

	Invoca resposta com todas as categorias exemplo resumido: 
	{'categories': {'href': 'https://api.spotify.com/v1/browse/categories?country=BR&offset=0&limit=50', 
	'items': [{'href': 'https://api.spotify.com/v1/browse/categories/toplists', 
	'icons': [{'height': 275, 'url': 'https://t.scdn.co/media/derived/toplists_11160599e6a04ac5d6f2757f5511778f_0_0_275_275.jpg', 
	'width': 275}], 
	'id': 'toplists', 'name': 'Top Lists'},
	"""
	def get_categories(self, country, limit):
		headers = self.get_resource_headers()
		endpoint = "https://api.spotify.com/v1/browse/categories"

		data = urlencode({"country" : country, "limit" :limit})
		loockup_id = f"{endpoint}?{data}"

		r = requests.get(loockup_id, headers = headers)
		if r.status_code not in range (200 , 299):
			return {}
		return r.json()


	"""
	##Faz o mesmo que o get_categories, porém já filtrado e como padrão Brasil e rock. 
	A FUNÇÃO NÃO PRECISA ESTÁ COMPLETA PARA FUNCIONAR
	
	"""
	def get_categoryByName(self, country = "BR", name = "rock"):

		headers = self.get_resource_headers()
		endpoint = "https://api.spotify.com/v1/browse/categories/" + name.lower()
		data = urlencode({"country": country})
		loockup_id = f"{endpoint}?{data}"
		r = requests.get(loockup_id, headers = headers)

		if r.status_code not in range (200 , 299):
			return {}
		return r.json()

	def get_recommendations(self, genres="rock"):
		headers  = self.get_resource_headers()
		endpoint = "https://api.spotify.com/v1/recommendations"
		data = urlencode({"seed_genres": genres})
		loockup_id = f"{endpoint}?{data}"
		r = requests.get(loockup_id, headers = headers)
		if r.status_code not in range (200 , 299):
			return {}
		return r.json()

	def search(self, query, search_type = 'artist'):
		#access_token = self.get_access_token()
		headers = self.get_resource_headers()

		endpoint = "https://api.spotify.com/v1/search"
		data = urlencode({"q":"Time", "type" : search_type.lower()})

		lock = f"{endpoint}?{data}"
		r = requests.get(lock, headers = headers)

		if r.status_code not in range (200 , 299):
			return {}
		return r.json()
	def profile(self, token):
		headers = {
			"Authorization" : f"Bearer {token}"
		}
		endpoint = "https://api.spotify.com/v1/me"
		#data = urlencode({'user_id'})
		lock = f"{endpoint}"
		r = requests.get(lock, headers = headers)
		return r.json()


	def getAuth(self):
		headers = {
			"client_id" : self.client_id, 
			"response_type" : "code", 
			"redirect_uri" : "http://127.0.0.1:5000/authorize", 
			"scope" :"user-read-private"
		}
		endpoint = "https://accounts.spotify.com/authorize"
		data = urlencode({"client_id" : self.client_id, "response_type" : "code", "redirect_uri" : "https://accounts.spotify.com/authorize", "scope" :"user-read-private"})

		lock = f"{endpoint}?{data}"
		r = requests.get(endpoint, params = headers)

		#print(r.text)
		return r.text

	def getCookies(self):
		session = requests.Session()
		
		response = session.get("https://accounts.spotify.com/pt-BR/login/")
		#print(session.cookies.get_dict())
		#print(response.headers)

#client_id = "08c1a6be652e4fdca07f1815bfd167e4"
#ORIGINAL - client_id = "a16059247336496a830d64cc548ae852"
#client_secret = "3cd7fd4c13fe433b9c16803dd8205a8a"



#t = spotifyAPI(client_id, client_secret)
#t.getCookies()
"""
for a in t.get_recommendations("sertanejo")['tracks']:
	for b in a['album']['artists']:
		print(a.get("name")," 	||  ", b.get("name"))
"""
