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
from wit import Wit

load_dotenv()

nest_asyncio.apply()
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
wit_client = Wit(os.getenv('wit'))
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
    await ctx.message.delete()
    confirm=client.get_channel(channel)
    await confirm.send("Channel set for updates")

@client.command(aliases=['link-insta'])
async def add_insta(ctx,*, account):
    global instagram_accounts
    await ctx.message.delete()
    instagram_accounts.append(account)
    await ctx.send(account+" added to the list")
    
@client.command(aliases=['unlink-insta'])
async def remove_insta(ctx,*,account):
    global instagram_accounts
    await ctx.message.delete()
    instagram_accounts.remove(account)
    await ctx.send(account+" removed from the list")

@client.command(aliases=["unlink-tweet"])
async def remove_tweet(ctx,*,account):
    global twitter_accounts
    await ctx.message.delete()
    twitter_accounts.remove(account)
    await ctx.send(account+ " removed from the list")

@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send("Pong\nLatency: "+str(client.latency*1000))

@client.command(aliases=["hi","hello","hey"])
async def greetings(ctx):
    await ctx.message.delete()
    greet_msgs = ["Hi {}!".format(ctx.author.name), "Hey {}!".format(ctx.author.name), "How are you {}?".format(ctx.author.name), "How's it going {}?".format(ctx.author.name)]
    await ctx.send(random.choice(greet_msgs))

client.remove_command("help")
@client.command(aliases=["use",'help','info'])
async def help_menu(ctx):
    embed = discord.Embed(title="Command Menu", color=color_var)
    await ctx.message.delete()
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
                await ctx.send(link)
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
    await ctx.message.delete()
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
    await ctx.message.delete()
    for each in new_tweets:
        link = "https://twitter.com/{username}/status/{id}".format(username=accountname, id = each.id)
        tweet_ids.append(each.id)
    await ctx.send(link)


@client.command(aliases=["tweet"])
async def fetch_tweets(ctx):
    global twitter_accounts, tweet_ids
    await ctx.message.delete()
    for twitter_account in twitter_accounts:
        new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
        for each in new_tweets:
            link = "https://twitter.com/{username}/status/{id}".format(username=twitter_account, id = each.id)
            await ctx.send(link)
            tweet_ids.append(each.id)

@client.command()
async def teval(ctx,*,text):
    user=InstagramUser("alvinalvinalvin437",sessionid=SESSIONID)
    await ctx.message.delete()
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
    await ctx.message.delete()
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
    await ctx.message.delete()
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
def ask_embed(title, answer):
    embed = discord.Embed(title=title, description=answer,color=color_var)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/849271520428949517/867430405497421864/logo.png")
    embed.set_author(name="EconHacks Bangalore", icon_url="https://media.discordapp.net/attachments/849271520428949517/867430405497421864/logo.png")
    return embed

@client.command(aliases=["ques"])
async def ask(ctx, *, question):
    resp = wit_client.message(question)
    await ctx.message.delete()
    try:
        intent = resp["intents"][0]["name"]
        confidence = resp["intents"][0]["confidence"]
        if confidence > 0.50:
            if intent == "Contact_organizers":
                embed = ask_embed("How Do I Contact The Organizers", "You can contact us on our email info@econhacksbangalore.live regarding any complaints, feedbacks and sugestions!")
                await ctx.send(embed=embed)
            elif intent == "Need_demo_":
                embed = ask_embed("Do We Need To Submit A Demo?", "idk. Need to ask Ansh regarding this")
                await ctx.send(embed=embed)
            elif intent == "Duration":
                embed = ask_embed("How Long Is The Hackathon?", "EconHacks is a 48 hour hackathon which starts on 1st October and ends on 3rd October")
                await ctx.send(embed=embed)
            elif intent == "How_much_does_it_cost_":
                embed = ask_embed("How Much Does It Cost?", "Zero. Zip. Zilch. Nada. Nothing. We have been able to bring this hackathon to you free of cost with the help of our amazing sponsors!")
                await ctx.send(embed=embed)
            elif intent == "Prizes":
                embed = ask_embed("Prizes", "There are over $1000 in the prizepool just waiting to be won!")
                await ctx.send(embed=embed)
            elif intent == "Register":
                embed = ask_embed("How Do I Register", "You can register using Devfolio!")
                await ctx.send(embed=embed)
            elif intent == "Sponsor":
                embed = ask_embed("Who Are The Sponsors", "This hackathon has been made possible by amazing sponsors Devfolio, Portis, Polygon, Tezos and Celo")
                await ctx.send(embed=embed)
            elif intent == "Team_or_individual":
                embed = ask_embed("Do We Participate Individually Or In Teams", "You can submit projects in teams of 1-5 peoplegoing solo is cool too! You can bring your friends as a team, or you can find team members at the event on our Discord server.")
                await ctx.send(embed=embed)
            elif intent == "Team_size":
                embed = ask_embed("How Big Can Teams Be", "You can submit projects in teams of 1-5 people. Most teams aim to have a mix of people with both design and developer skills.")
                await ctx.send(embed=embed)
            elif intent == "What_can_we_build":
                embed = ask_embed("Theme Of The Hackathon", "This is an Economy based hackathon. You can build anything which provides an economic value and helps the struggling citizens of our country.")
                await ctx.send(embed=embed)
            elif intent == "What_is_a_hackathon":
                embed = ask_embed("What Is A Hackathon", "A hackathon is best described as an “invention marathon”. Anyone who has an interest in technology attends a hackathon to learn, build & share their creations over the course of a weekend in a relaxed and welcoming atmosphere. You don’t have to be a programmer and you certainly don’t have to be majoring in Computer Science.")
                await ctx.send(embed=embed)
            elif intent == "Who_can_take_part":
                embed = ask_embed("Who Can Take Part", "All high school students are eligible to participate in this awesome hackathon!")
                await ctx.send(embed=embed)
    except:
        await ctx.send("I didn't get that. Need to be retrained.")
        print(question)

client.run(os.getenv('token'))