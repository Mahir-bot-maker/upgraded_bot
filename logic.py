import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self,pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number= random.randint(1,1300)
        self.name = None
        self.img = None
        self.attack = None
        self.defense = None
        self.hp = None

    async def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["forms"][0]["name"]
                else:
                    return "Pikachu"
 
                
    async def show_img(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["sprites"]["front_default"]
                else:
                    return None
                
    
