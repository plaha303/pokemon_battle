import asyncio
import aiohttp
import random

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

pokemon_list = ['pikachu', 'charmander', 'bulbasaur', 'squirtle', 'jigglypuff',
                'meowth', 'psyduck', 'snorlax', 'magikarp', 'eevee']


async def fetch_pokemon_data(session, pokemon_name):
    try:
        async with session.get(f"{POKEAPI_URL}{pokemon_name}", timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "name": data["name"],
                    "attack": data["stats"][1]["base_stat"],
                    "defense": data["stats"][2]["base_stat"],
                    "speed": data["stats"][5]["base_stat"],
                }
            else:
                print(f"Failed to fetch data for {pokemon_name} with status {response.status}")
                return None
    except Exception as e:
        print(f"Failed to fetch data for {pokemon_name}: {e}")
        return None


async def get_all_pokemon_data(pokemon_names):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon_data(session, name) for name in pokemon_names]
        return await asyncio.gather(*tasks)


def calculate_strength(pokemon):
    return pokemon["attack"] + pokemon["defense"] + pokemon["speed"]


def battle(pokemon1, pokemon2):
    strength1 = calculate_strength(pokemon1)
    strength2 = calculate_strength(pokemon2)

    print(f"Battle between {pokemon1['name']} and {pokemon2['name']}")
    print(
        f"{pokemon1['name']} stats - Attack: {pokemon1['attack']}, Defense: {pokemon1['defense']}, Speed: {pokemon1['speed']}, Strength: {strength1}")
    print(
        f"{pokemon2['name']} stats - Attack: {pokemon2['attack']}, Defense: {pokemon2['defense']}, Speed: {pokemon2['speed']}, Strength: {strength2}")

    if strength1 > strength2:
        print(f"Winner: {pokemon1['name']}!\n")
        return pokemon1['name']
    elif strength2 > strength1:
        print(f"Winner: {pokemon2['name']}!\n")
        return pokemon2['name']
    else:
        print("It's a tie!\n")
        return "Tie"


async def main():
    pokemon_data = await get_all_pokemon_data(pokemon_list)

    pokemon_data = [p for p in pokemon_data if p is not None]

    if len(pokemon_data) >= 2:
        pokemon1, pokemon2 = random.sample(pokemon_data, 2)
        battle(pokemon1, pokemon2)
    else:
        print("Not enough Pokémon data available for a battle.")

asyncio.run(main())
