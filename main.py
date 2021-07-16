import discord
from discord.ext import commands, tasks
import json
import random
from instagramy import *
from instascrape import *
import os
import twint
import nest_asyncio
from sessID import *
nest_asyncio.apply()
twitter_update_channel = 865429347594403850
default_prefix="h!"
color_var=discord.Color.from_rgb(0, 235, 0)
prefix={}

global channel, SESSIONID
channel=0
SESSIONID=""
old_posts=[]
client=commands.Bot(command_prefix=default_prefix)

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

@client.event
async def on_ready():
    print("Ready")
    instag.start()
@client.command()
async def link(ctx,chann:discord.TextChannel):
    global channel
    channel=chann.id
    confirm=client.get_channel(channel)
    await confirm.send("Channel set for instagram updates")
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
    global channel, old_posts, SESSIONID
    if channel!=0:
        try:
            user=InstagramUser("testforhackathonbot",sessionid=SESSIONID)
            print(user)
            url=user.posts[0].post_url
            if not url in old_posts:
                old_posts+=[url]
                cha=client.get_channel(channel)
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
                await cha.send(embed=embed)
        except:
            SESSIONID=get_it()
@instag.before_loop
async def wait_for_ready():
    await client.wait_until_ready()
@client.command()
async def insta(ctx):
    global SESSIONID
    try:
        user=InstagramUser("testforhackathonbot",sessionid=SESSIONID)
        print(user)
        url=user.posts[0].post_url
        pos=Post(url)
        headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        "cookie": SESSIONID}
        pos.scrape(headers=headers)    
        descript=pos.caption
        thumb=user.profile_picture_url
        embed=discord.Embed(title="Insta",description=descript, color=color_var)
        embed.set_image(url=user.posts[0].post_source)
        embed.set_thumbnail(url=thumb)
        await ctx.send(embed=embed)
    except:
        SESSIONID=get_it()
@client.command(aliases=["tweet"])
async def fetch_tweets(ctx):
    new_tweets = api.user_timeline(screen_name="@Paz50982472",count=1, tweet_mode="extended")
    for each in new_tweets:
        latest_tweet = each.text
    latest_tweet_id = 0
    for each in new_tweets:
        if 'media' in each.entities:
            for image in  each.entities['media']:
                latest_img = image['media_url'])
    #update_channel = client.get_channel(twitter_update_channel)
    #await update_channel.send(tlist)
    
file = open("../env.txt","r")
txt_from_file = str(file.read())
start_token = txt_from_file.find("token=") + len("token=")
end_token = txt_from_file.find('"',start_token + 3) + 1
client.run(eval(txt_from_file[start_token:end_token]))




