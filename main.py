import discord
from discord.ext import commands, tasks
import json
import random
from instagramy import *
from instascrape import *
import os
import tweepy
import nest_asyncio
from dotenv import load_dotenv
from sessID import *

load_dotenv()

nest_asyncio.apply()
twitter_update_channel = 865429347594403850
default_prefix="h!"
color_var=discord.Color.from_rgb(0, 235, 0)
prefix={}

global channel, SESSIONID, latest_tweet_id
latest_tweet_id = 0
channel=0
SESSIONID=""
Media_present = False
Extended_entites_present = False
old_posts=[]
client=commands.Bot(command_prefix=default_prefix)
if True:
    consumer_key = os.getenv('consumer_key')
    consumer_secret = os.getenv('consumer_secret')
    access_key = os.getenv('access_key')
    access_secret = os.getenv('access_secret')

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
@tasks.loop(minutes=1)
async def instag():
    global channel, old_posts, SESSIONID, latest_tweet_id
    print(old_posts)
    print(channel)
    new_tweets = api.user_timeline(screen_name="@Microsoft",count=1, tweet_mode="extended")
    if channel!=0:
        print(new_tweets[0].id)
        if new_tweets[0].id != latest_tweet_id:
            for each in new_tweets:
                Media_present = False
                Extended_entites_present = False
                try:
                     if "extended_entities" in dir(new_tweets[0]):
                        Extended_entites_present = True
                except:
                    pass
                try:
                    if "media" in dir(new_tweets[0].entities):
                        Media_present = True
                except:
                    pass
                cha = client.get_channel(channel)
                latest_tweet_id = each.id
                latest_tweet = new_tweets[0].full_text
                if Extended_entites_present == True or Media_present == True:
                    embed=discord.Embed(title="Microsoft",description=latest_tweet, color=color_var)
                    embed.set_thumbnail(url=new_tweets[0].user.profile_image_url)
                    try:
                        if len(each.extended_entities['media']) > 1:
                            await cha.send(embed=embed)
                            for image in each.extended_entities['media']:
                                latest_img = image['media_url']
                                embed=discord.Embed(color=color_var)
                                embed.set_image(url=latest_img)
                                await cha.send(embed=embed)
                    except:
                        for image in each.entities['media']:
                            embed.set_image(url=latest_img)
                            await cha.send(embed=embed)
                else:
                    embed=discord.Embed(title="Microsoft",description=latest_tweet, color=color_var)
                    embed.set_thumbnail(url=new_tweets[0].user.profile_image_url)
                    await cha.send(embed=embed)
    #update_channel = client.get_channel(twitter_update_channel)
    #await update_channel.send(tlist)
        try:
            user=InstagramUser("alvinalvinalvin437",sessionid=SESSIONID)
            print(len(user.posts))
            url=user.posts[0].post_url
            if not url in old_posts:                
                cha=client.get_channel(channel)
                pos=Post(url)
                headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
                "cookie": "sessionid="+SESSIONID+";"}
                pos.scrape(headers=headers)    
                descript=pos.caption
                thumb=user.profile_picture_url
                embed=discord.Embed(title="Insta",description=descript, color=color_var)
                embed.set_image(url=user.posts[0].post_source)
                embed.set_thumbnail(url=thumb)
                await cha.send(embed=embed)
                old_posts+=[url]
        except Exception as e:
            print(e)
            SESSIONID=get_it()
            print(SESSIONID)
@instag.before_loop
async def wait_for_ready():
    await client.wait_until_ready()
@client.command()
async def insta(ctx):
    global SESSIONID
    try:
        user=InstagramUser("alvinalvinalvin437",sessionid=SESSIONID)
        print(user)
        url=user.posts[0].post_url
        pos=Post(url)
        headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        "cookie": "sessionid="+SESSIONID+";"}
        pos.scrape(headers=headers)    
        descript=pos.caption
        thumb=user.profile_picture_url
        embed=discord.Embed(title="Insta",description=descript+"\nLikes: "+str(user.posts[0].likes)+"\nComments: "+str(user.posts[0].likes), color=color_var)
        embed.set_image(url=user.posts[0].post_source)
        embed.set_thumbnail(url=thumb)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        SESSIONID=get_it()
        print(SESSIONID)
@client.command(aliases=["tweet"])
async def fetch_tweets(ctx):
    global latest_tweet_id 
    Media_present = False
    Extended_entites_present = False
    new_tweets = api.user_timeline(screen_name="@Paz50982472",count=1, tweet_mode="extended")
    try:
        if "extended_entities" in dir(new_tweets[0]):
            Extended_entites_present = True
    except:
        pass
    try:
        if "media" in dir(new_tweets[0].entities):
            Media_present = True
    except:
        pass
    for each in new_tweets:
        latest_tweet = each.full_text
        if Extended_entites_present == True or Media_present == True:
            embed=discord.Embed(title="@Paz50982472",description=latest_tweet, color=color_var)
            latest_tweet_id = each.id
            embed.set_thumbnail(url=new_tweets[0].user.profile_image_url)
            try:
                if len(each.extended_entities['media']) > 1:
                    await ctx.send(embed=embed)
                    for image in each.extended_entities['media']:
                        latest_img = image['media_url']
                        embed=discord.Embed(color=color_var)
                        embed.set_image(url=latest_img)
                        latest_tweet_id = new_tweets[0].id
                        await ctx.send(embed=embed)
            except:
                for image in each.entities['media']:
                    embed.set_image(url=latest_img)
                    latest_tweet_id = new_tweets[0].id
                    await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="@Paz50982472",description=latest_tweet, color=color_var)
            embed.set_thumbnail(url=new_tweets[0].user.profile_image_url)
            latest_tweet_id = new_tweets[0].id
            await ctx.send(embed=embed)
    #update_channel = client.get_channel(twitter_update_channel)
    #await update_channel.send(tlist)
@client.command()
async def teval(ctx,*,text):
    user=InstagramUser("alvinalvinalvin437",sessionid=SESSIONID)        
    url=user.posts[0].post_url
    pos=Post(url)
    headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid="+SESSIONID+";"}
    try:
        await ctx.send("```\n"+str(eval(text))+"\n```")
    except Exception as e:
        await ctx.send(str(e))
@client.command()
async def say(ctx, chann:discord.TextChannel,*,say):
    await chann.send(str(say))        

client.run(os.getenv('token'))