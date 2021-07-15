import discord
from discord.ext import commands, tasks
import json
import os
import token
intent=discord.Intents.default()
intent.members=True
default_prefix="h!"
prefix={}
client=commands.Bot(command_prefix=default_prefix,intents=intent)
os.environ(token)
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("Pong\nLatency: "+client.latency)
@client.command(aliases=["hi","hello","hey"])
async def greetings(ctx):   
    greet_msgs = ["Hi {}!".format(ctx.author.name), "Hey {}!".format(ctx.author.name), "How are you {}?".format(ctx.author.name), "How's it going {}?".format(ctx.author.name)]


@client.command(aliases=["use",'help','info'])
async def help_menu(ctx):
    embed = discord.Embed(title="Command Menu", color=discord.Color.from_rgb(0, 235, 0))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/858234706305482785/865191551444844544/hackathonlogo.png")
    embed.set_thumbnail(name="Social",value="h!insta to get insta feed\nh!tweet to get twitter feed")
    embed.set_thumbnail(name="Events", value="h!hdt to get hackathon dates")
    embed.set_thumbnail(name="Questions", value="h!FAQ to drop your questions and our team will answer")
    embed.set_thumbnail(name="Addtional Queries", value="`ansh@econhacks.org`")
    await ctx.send(embed=embed)

client.run("token")
