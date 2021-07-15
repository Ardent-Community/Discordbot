import discord
from discord.ext import commands, tasks
import json
import random
from instagramy import *
from instascrape import *
import os
default_prefix="h!"
color_var=discord.Color.from_rgb(0, 235, 0)
prefix={}
global mess
mess=None
client=commands.Bot(command_prefix=default_prefix)

@client.event
async def on_ready():
    print("Ready")
    instag.start()
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
@tasks.loop(seconds=5)
async def instag():
    global mess
    if mess!=None:
        user=InstagramUser("testforhackathonbot",sessionid="48297384187%3AYfiE4AoNcVSsdQ%3A26")
        print(user)
        url=user.posts[0].post_url
        pos=Post(url)
        headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        "cookie": "sessionid=48297384187%3AYfiE4AoNcVSsdQ%3A26;"}
        pos.scrape(headers=headers)    
        descript=pos.caption
        thumb=user.profile_picture_url
        embed=discord.Embed(title="Insta",description=descript, color=color_var)
        embed.set_image(url=user.posts[0].post_source)
        embed.set_thumbnail(url=thumb)
        await mess.edit(embed=embed)
@instag.before_loop
async def wait_for_ready():
    await client.wait_until_ready()
@client.command()
async def insta(ctx):
    global mess
    user=InstagramUser("testforhackathonbot",sessionid="48297384187%3AYfiE4AoNcVSsdQ%3A26")
    print(user)
    url=user.posts[0].post_url
    pos=Post(url)
    headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid=48297384187%3AYfiE4AoNcVSsdQ%3A26;"}
    pos.scrape(headers=headers)    
    descript=pos.caption
    thumb=user.profile_picture_url
    embed=discord.Embed(title="Insta",description=descript, color=color_var)
    embed.set_image(url=user.posts[0].post_source)
    embed.set_thumbnail(url=thumb)
    mess=await ctx.send(embed=embed)
    
file = open("../env.txt","r")
txt_from_file = str(file.read())
start_token = txt_from_file.find("token=") + len("token=")
end_token = txt_from_file.find('"',start_token + 3) + 1
client.run(eval(txt_from_file[start_token:end_token]))




