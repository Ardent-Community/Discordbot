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

global channel, SESSIONID, latest_tweet_id, roles_allowed, instagram_accounts, twitter_accounts
roles_allowed=[]

latest_tweet_id = 0
channel=0
SESSIONID=""
Media_present = False
Extended_entites_present = False
old_posts=[]
instagram_accounts=[]
twitter_accounts = []
tweet_ids = []

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
    await confirm.send("Channel set for updates")
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
@client.command(aliases=["unlink-tweet"])
async def remove_tweet(ctx,*,account):
    global twitter_accounts
    twitter_accounts.remove(account)
    await ctx.send(account+ " removed from the list")
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
    global channel, old_posts, SESSIONID, tweet_ids, twitter_accounts, instagram_accounts
    print("loop")
    cha = client.get_channel(channel)
    if channel!=0:
    #twitter
        for twitter_account in twitter_accounts:
            new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
            print(new_tweets[0].id, tweet_ids)
            if new_tweets[0].id not in tweet_ids:
                link = "https://twitter.com/{username}/status/{id}".format(username=twitter_account, id = new_tweets[0].id)
                ctx.send(link)
                tweet_ids.append(new_tweets[0].id)

    #instagram
        for i_ac in instagram_accounts:
            try:
                embed=instagram_get(i_ac)
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

@client.command(aliases=["link-tweet"])
async def link_tweets(ctx, *, accountname):
    global twitter_accounts, tweet_ids
    new_tweets = api.user_timeline(screen_name=accountname,count=1, tweet_mode="extended")
    twitter_accounts.append(accountname)
    for each in new_tweets:
        link = "https://twitter.com/{username}/status/{id}".format(username=accountname, id = each.id)
        tweet_ids.append(each.id)
    await ctx.send(link)


@client.command(aliases=["tweet"])
async def fetch_tweets(ctx):
    global twitter_accounts, tweet_ids
    for twitter_account in twitter_accounts:
        new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
        for each in new_tweets:
            link = "https://twitter.com/{username}/status/{id}".format(username=twitter_account, id = each.id)
            await ctx.send(link)
            tweet_ids.append(each.id)

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
