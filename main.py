from logic import Pokemon
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

@piton.event
async def on_member_join(member):
    # Karşılama mesajı gönderme
    for channel in member.guild.text_channels:
        await channel.send (f" Hoş geldiniz:, {member.mention}!")

    
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
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")
piton.run (TOKEN)