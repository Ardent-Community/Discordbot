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

global channel, SESSIONID, latest_tweet_id, roles_allowed, instagram_accounts
roles_allowed=[]
latest_tweet_id = 0
channel=0
SESSIONID=""
Media_present = False
Extended_entites_present = False
old_posts=[]
instagram_accounts=[]


client=commands.Bot(command_prefix=default_prefix)

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_key = os.getenv('access_key')
access_secret = os.getenv('access_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
def instagram_get(account, not_loop=False):
    global SESSIONID, old_posts
    try:
        user=InstagramUser(account,sessionid=SESSIONID)
        print(len(user.posts))
        url=user.posts[0].post_url
        if (not url in old_posts) or not_loop:                
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
            if not not_loop:
                old_posts+=[url]
            return embed
        
                
    except Exception as e:
        print(e)
        SESSIONID=get_it()
        print(SESSIONID)
        
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
@client.command(aliases=['link-insta'])
async def add_insta(ctx,*, account):
    global instagram_accounts
    instagram_accounts.append(account)
    await ctx.send(account+" added to the list")
@client.command(aliases=['unlink-insta'])
async def remove_insta(ctx,*,account):
    global instagram_accounts
    instagram_accounts.remove(account)
    await ctx.send(account+" removed from the list")
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
    global channel, old_posts, SESSIONID, latest_tweet_id, twitter_account, instagram_accounts
    print("loop")
    cha = client.get_channel(channel)
    if channel!=0:
        #twitter
        try:
            new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
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
                    latest_tweet_id = each.id
                    latest_tweet = new_tweets[0].full_text
                    if Extended_entites_present == True or Media_present == True:
                        embed=discord.Embed(title=str(twitter_account),description=latest_tweet, color=color_var)
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
                        embed=discord.Embed(title=twitter_account,description=latest_tweet, color=color_var)
                        embed.set_thumbnail(url=new_tweets[0].user.profile_image_url)
                        await cha.send(embed=embed)
        except:
            pass
    #instagram
        for i_ac in instagram_accounts:
            try:                
                embed=instagram_get(i_ac)
                print(embed)
                if embed!=None:
                    await cha.send(embed=embed)
            except Exception as e:
                print(e)
                await cha.send("This account "+i_ac+" may not exist")
            
            
@instag.before_loop
async def wait_for_ready():
    await client.wait_until_ready()

@client.command()
async def insta(ctx):
    global instagram_accounts
    for i in instagram_accounts:
        try:
            embed=instagram_get(i,True)
            if embed!=None:
                await ctx.send(embed=embed)
        except:
            await ctx.send("The account "+i+" may not exist")
def twitter_post(account):
    pass
    
@client.command(aliases=["link-tweet"])
async def link_tweets(ctx, *, account):
    global latest_tweet_id, twitter_account
    Media_present = False
    twitter_account = account
    Extended_entites_present = False
    new_tweets = api.user_timeline(screen_name=account,count=1, tweet_mode="extended")
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
            embed=discord.Embed(title=account,description=latest_tweet, color=color_var)
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
            embed=discord.Embed(title=account,description=latest_tweet, color=color_var)
            embed.set_thumbnail(url=new_tweets[0].user.profile_image_url)
            latest_tweet_id = new_tweets[0].id
            await ctx.send(embed=embed)


@client.command(aliases=["tweet"])
async def fetch_tweets(ctx):
    global latest_tweet_id, twitter_account
    Media_present = False
    Extended_entites_present = False
    new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
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
            embed=discord.Embed(title=twitter_account,description=latest_tweet, color=color_var)
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
            embed=discord.Embed(title=twitter_account,description=latest_tweet, color=color_var)
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
    global roles_allowed
    for i in roles_allowed:
        if discord.utils.get(ctx.guild.roles, id=i) in ctx.author.roles:
            await chann.send(str(say))
            break
    else:
        await ctx.send("Access Denied")
@client.command()
@commands.has_permissions(manage_messages=True)
async def role(ctx, mode="", *, role_name=""):
    global roles_allowed    
    if mode.lower()=="set":
        if role_name in [i.name for i in ctx.guild.roles]:
            the_role=discord.utils.get(ctx.guild.roles, name=role_name).id
            roles_allowed+=[the_role]
            await ctx.send(role_name+" can access say command")
    elif mode.lower()=="remove":
        the_role=discord.utils.get(ctx.guild.roles, name=role_name).id
        roles_allowed.remove(the_role)
        await ctx.send(role_name+" can no longer access say command")
    else:
        st=""
        for i in roles_allowed:
            st=st+str(discord.utils.get(ctx.guild.roles,id=i).name)+"\n"
        await ctx.send(embed=discord.Embed(title="Roles allowed", description=st,color=color_var))     

client.run(os.getenv('token'))
