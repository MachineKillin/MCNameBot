import aiohttp
import discord
from discord.ext import commands
from discord.ext import tasks

client = discord.Client()
intents = discord.Intents.default()
bot = commands.Bot

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$check "):
    username = msg.split("$check ",1)[1]
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{username}') as resp:
            request = await resp.json(content_type=None)
    if resp.status != 200:
        await message.channel.send("Name is **Not** taken!")
    else:
        ign = request['name']
        uuid = request['id']
        await message.channel.send("The name {} is taken! (uuid: `{}`) NameMC: https://namemc.com/profile/{}".format(ign, uuid, ign))

client.run("Token")