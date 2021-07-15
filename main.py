import discord
from discord.ext import commands, tasks
import json
import os
intent=discord.Intents.default()
default_prefix="h!"
prefix={}
client=commands.Bot(command_prefix=default_prefix)
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("Pong\nLatency: "+str(client.latency*1000))

client.run("token")
