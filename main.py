import discord
from discord.ext import commands, tasks
import json
import random
from instagramy import *
import os
default_prefix="h!"
color_var=discord.Color.from_rgb(0, 235, 0)
prefix={}
client=commands.Bot(command_prefix=default_prefix)
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("Pong\nLatency: "+str(client.latency*1000))
@client.command(aliases=["hi","hello","hey"])
async def greetings(ctx):   
    greet_msgs = ["Hi {}!".format(ctx.author.name), "Hey {}!".format(ctx.author.name), "How are you {}?".format(ctx.author.name), "How's it going {}?".format(ctx.author.name)]
    await ctx.send(random.choice(greet_msgs))
client.remove_command("help")
@client.command(aliases=["use",'help','info'])
async def help_menu(ctx):
    embed = discord.Embed(title="Command Menu", color=color_var)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/858234706305482785/865191551444844544/hackathonlogo.png")
    embed.add_field(name="Social",value="h!insta to get insta feed\nh!tweet to get twitter feed")
    embed.add_field(name="Events", value="h!hdt to get hackathon dates")
    embed.add_field(name="Questions", value="h!FAQ to drop your questions and our team will answer")
    embed.add_field(name="Addtional Queries", value="`ansh@econhacks.org`")
    await ctx.send(embed=embed)
@client.command()
async def insta(ctx):
    user=InstagramUser("testforhackathonbot")
    print(user)
    descript=user.posts[0].caption
    thumb=user.profile_picture_url
    embed=discord.Embed(title="Insta",description=descript, color=color_var)
    embed.set_image(url=user.posts[0].post_source)
    embed.set_thumbnail(url=thumb)
    await ctx.send(embed=embed)
    
file = open("../env.txt","r")
txt_from_file = str(file.read())
start_token = txt_from_file.find("token=") + len("token=")
end_token = txt_from_file.find('"',start_token + 3) + 1
client.run(eval(txt_from_file[start_token:end_token]))




