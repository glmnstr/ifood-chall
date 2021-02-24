from teste import spotifyAPI

"""
If temperature (celcius) is above 30 degrees, suggest tracks for party
In case temperature is between 15 and 30 degrees, suggest pop music tracks
If it's a bit chilly (between 10 and 14 degrees), suggest rock music tracks
Otherwise, if it's freezing outside, suggests classical music tracks
"""


class system():
	client_id = "08c1a6be652e4fdca07f1815bfd167e4"
	#ORIGINAL - client_id = "a16059247336496a830d64cc548ae852"
	client_secret = "3cd7fd4c13fe433b9c16803dd8205a8a"

	def get_playlist(self, temperatura):
		sptAPI = spotifyAPI(self.client_id, self.client_secret)
		if temperatura != None:
			if temperatura > 31:
				return sptAPI.get_recommendations("party")
			elif temperatura in range(15, 30):
				return sptAPI.get_recommendations("pop")
			elif temperatura in range(10, 14):
				return sptAPI.get_recommendations("rock")
			else:
				return sptAPI.get_recommendations("classical")
		else:
			return "Erro na classe System!!"

t = system()
t.get_playlist(29)
