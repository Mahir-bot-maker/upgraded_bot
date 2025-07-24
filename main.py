from logic import Pokemon
import random
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("DISCORD_BOT")

import discord
from discord.ext import commands

izinler = discord.Intents.all()
izinler.message_content = True
izinler.members = True

piton = commands.Bot(command_prefix="/", intents=izinler)

@piton.event
async def on_ready():
    print(f"{piton.user.name} is ready")

@piton.command("at")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("senden büyüğü atamazsın")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"{member.name} atıldı")
    else:
        await ctx.send("atmak istediğiniz kullanıcıyı belirtin")

@piton.command("go")
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)
        pokemon.set_stats()
        Pokemon.pokemons[author] = pokemon
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")


@piton.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.perform_attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")



class Fighter(Pokemon):
    # Pokemon sınıfından miras alan bir Dövüşçü alt sınıfı
    async def perform_attack(self, enemy):
        # Temel saldırıyı ekstra güç ekleyerek geliştiren bir metot
        super_power = random.randint(5, 15)
        self.attack  += super_power
        result = await super().perform_attack(enemy)  # Ekstra güç ile temel saldırıyı çağırma
        self.attack -= super_power    # Saldırı gücünü saldırıdan sonra orijinal değerine döndürme
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"


piton.run(TOKEN)
