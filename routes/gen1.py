import requests

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
