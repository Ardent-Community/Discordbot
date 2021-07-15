import discord
from discord.ext import commands, tasks
import json
import random

import os
default_prefix="h!"
prefix={}
client=commands.Bot(command_prefix=default_prefix)
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("Pong\nLatency: "+str(client.latency*1000))
@client.command(aliases=["hi","hello","hey"])
async def greetings(ctx):   
    greet_msgs = ["Hi {}!".format(ctx.author.name), "Hey {}!".format(ctx.author.name), "How are you {}?".format(ctx.author.name), "How's it going {}?".format(ctx.author.name)]
    await ctx.send(random.choice(greet_msgs))
@client.command
file = open("../env.txt","r")
txt_from_file = str(file.read())
start_token = txt_from_file.find("token=") + len("token=")
end_token = txt_from_file.find('"',start_token + 3) + 1
client.run(eval(txt_from_file[start_token:end_token]))

