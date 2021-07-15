import discord
from discord.ext import commands, tasks
import json
intent=discord.Intents.default()
intent.members=True
default_prefix="h!"
prefix={}
client=commands.Bot(command_prefix=default_prefix,intents=intent)
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("Pong\nLatency: "+client.latency)
@client.command(aliases=["hi","hello","hey"])
async def greetings(ctx):   
    greet_msgs = ["Hi {}!".format(ctx.author.name), "Hey {}!".format(ctx.author.name), "How are you {}?".format(ctx.author.name), "How's it going {}?".format(ctx.author.name)]

client.run("token")
