import discord
from discord.ext import commands, tasks
import json
import os
intent=discord.Intents.default()
intent.members=True
default_prefix="h!"
prefix={}
client=commands.Bot(command_prefix=default_prefix,intents=intent)
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("Pong\nLatency: "+client.latency)
client.run("token")
