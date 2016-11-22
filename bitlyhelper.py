import urllib
import json

TOKEN="cc922578a7a1c6065a2aa91bc62b02e41a99afdb"
ROOT_URL="https://api-ssl.bitly.com"
SHORTEN="/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

	def shorten_url(self,longurl):
		try:
			url=ROOT_URL + SHORTEN.format(TOKEN, longurl)
			print(url)
			response=urllib.request.urlopen(url).read()
			jr = json.loads(response.decode('utf-8') )
			shorted = jr['data']['url']
			if shorted:
				return shorted
		except Exception as e:
			print(e)

		return longurl

