import discord, json
from discord.ext import commands
from json import load
import time 
import random

with open('config.json') as f:
    d = load(f)
    token = d["token"]
    prefix = d["prefix"]

bot = commands.Bot(command_prefix=prefix, self_bot=True,  help_command=None, fetch_offline_members=False)

@bot.command()
async def bump(ctx):
    user = ctx.author
    await ctx.send(f'通知します<@{user.id}>')
    time.sleep(random.randint(7205, 7210))
    while True:
        await ctx.send(f'<{user.id}>')
        time.sleep(random.randint(7205, 7210))
print("ok,success login")
bot.run(token, bot=False)