from flask import Flask, jsonify, render_template
import requests
from typing import List, Dict, Any


app = Flask(__name__)


def get_gen1_pokemon_data():

    pokemon_list = []
    base_url = "https://pokeapi.co/api/v2/pokemon"
    
    
    for pokemon_id in range(1, 152):  # Grab the OG 151
        try:
			# construct the url for call
            url = f"{base_url}/{pokemon_id}"
			# make the call, adding a timeout condition
            response = requests.get(url, timeout=15)
            
            # successfull call
            if response.status_code == 200:
                data = response.json()
                
                # Extract abilities
                abilities = []
                for ability in data.get('abilities', []):
                    abilities.append({
                        'name': ability['ability']['name'],
                        'is_hidden': ability['is_hidden'],
                        'slot': ability['slot']
                    })
                
                # Extract types
                types = [type_info['type']['name'] for type_info in data.get('types', [])]
                
                # Get image URLs
                sprites = data.get('sprites', {})
                images = {
                    'official_artwork': sprites.get('other', {}).get('official-artwork', {}).get('front_default'),
                    'front_default': sprites.get('front_default'),
                    'front_shiny': sprites.get('front_shiny')
                }
                
                # Create Pokemon data struct
                pokemon_data = {
                    'id': data['id'],
                    'name': data['name'].capitalize(), # capitalize the first letter
                    'abilities': abilities,
                    'types': types,
                    'images': images,
                    'height': data['height'],
                    'weight': data['weight'],
                    'base_experience': data['base_experience']
                }
                
                # adding struct to the array of pokemon
                pokemon_list.append(pokemon_data)
				
				# print successful capture
                print(f"Fetched {pokemon_data['name']} (ID: {pokemon_id})")
                
            else:
				# debug failure
                print(f"Failed to fetch Pokemon ID {pokemon_id}")
                
        except requests.RequestException as e:
            print(f"Error fetching Pokemon ID {pokemon_id}: {e}")
            continue
    
    return pokemon_list


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
def get_pokemon(name: str):

	url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
	try:
		# try to get a response
		resp = requests.get(url, timeout=15)
	except requests.RequestException:
		return jsonify({"error": "Upstream request failed"}), 502

	# possible error if bad name or somthing like that, 404 is not found.
	if resp.status_code != 200:
		return jsonify({"error": "Pokémon not found"}), 404

	# store our response as a json object.
	data = resp.json()

	# dictionary to analyze our response returned from the API call.
	result = {
		"id": data.get("id"),
		"name": data.get("name"),
		"abilities": [],
		"types": []
	}
	
	# iterate abilities
	abilities_data = data.get("abilities") or []
	for ability in abilities_data:
		ability_info = {
			"name": (ability.get("ability") or {}).get("name"),
			"is_hidden": ability.get("is_hidden"),
			"slot": ability.get("slot"),
		}
		result["abilities"].append(ability_info)
	
	# iterate types
	types_data = data.get("types") or []
	for type_info in types_data:
		type_name = (type_info.get("type") or {}).get("name")
		result["types"].append(type_name)

	# return the result as a json object.
	return jsonify(result)


if __name__ == "__main__":

	app.run(host="0.0.0.0", port=5000, debug=True)


