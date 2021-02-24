import requests
import json

api_token = "a123fac8ad0b7f9c3eff67758a0ad250"

url = "http://api.ipstack.com/"
ip = "189.114.148.246"
param = {
	"access_key" : api_token
}
req = requests.get(url + ip, params = param)
print (req.json())
