import os
from apifier import Apifier

path = os.path.dirname(os.path.realpath(__file__)) + os.sep
description_file = path + "lefigaro.json"

# Using a file descriptor
api = Apifier(description_file=description_file)
print(api.load())

# Using a config dictionnary
config = {
    "name": "Top Biere France",
    "url": "http://www.paradis-biere.com/top-biere.html",
    "description": {
	    "name": "div.bienvenue > table tr:nth-child(1n + 2) > td:nth-child(1) a",
	    "brewery": "div.bienvenue > table tr:nth-child(1n + 2) > td:nth-child(2)",
	    "country": "div.bienvenue > table tr:nth-child(1n + 2) > td:nth-child(3)",
	    "rating": "div.bienvenue > table tr:nth-child(1n + 2) > td:nth-child(4)"
    }
}
api = Apifier(config=config)
print(api.load())
