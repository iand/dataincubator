import urllib2
import json
import convert
#JSON_URI = "http://openlibrary.org/recentchanges.json"
JSON_URI = "file:///home/kier/openlibrary/recentchanges.json"
def convert_recent(recch):
	data = convert.download(recch)
	keys = [("http://openlibrary.org" + x["key"] + ".json") for x in data if x["key"].startswith("/b/")]
	convert.convert(keys)
if __name__ == "__main__":
	convert_recent(JSON_URI)
