import json
from urllib.request import urlopen

def getjson(url):
    return json.loads(urlopen(url).read().decode("utf-8"))

def search(keyword):
    result = getjson("https://api.duckduckgo.com/?q="+keyword+"&format=json")
    results = []
    for key in result["RelatedTopics"]:
      if "Result" in key:
        results.append(key["Result"])
    return results


print(search("Hamburger"))