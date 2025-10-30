from flask import Flask, jsonify, render_template
import requests
from typing import List, Dict, Any
from routes.gen1 import get_gen1_pokemon_data
from routes.index import get_pokemon


app = Flask(__name__)

# Root route! It will render the index.html template that we've created!
@app.get("/")
def index():
	return render_template("index.html")

# Gen 1 route! It will render the gen1.html template with all 151 Pokemon, 
@app.get("/gen1")
def gen1():
	# Fetch all Gen 1 Pokemon data
	pokemon_data = get_gen1_pokemon_data()
	# Render gen1 template with the pokemon data being passed into it from Flask, please read how Flask is handling this
	return render_template("gen1.html", pokemon_list=pokemon_data)

# This is the API route! It will return a JSON response from our call. 502 is bad gateway. set the timeout to 15 seconds but can change as needed
@app.get("/api/pokemon/<string:name>")
def searchPokemon(name):
	pokemonData = get_pokemon(name)
	return pokemonData
	
if __name__ == "__main__":

	app.run(host="0.0.0.0", port=5000, debug=True)


