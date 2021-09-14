import discord
from discord.ext import commands, tasks
from discord_components import *           #pip install discord-components
import asyncio
from discord.ext.commands import bot
from discord.utils import get
import json
import random
import cv2
import requests
import numpy as np
from instagramy import *
from instascrape import *
import os
from prsaw import RandomStuff
import tweepy
import nest_asyncio
from dotenv import load_dotenv
from sessID import *
from wit import Wit
import sys
import emoji
from replit import db
load_dotenv()

CBAPI= os.getenv("cbapi")
nest_asyncio.apply()
default_prefix="h!"
color_var=discord.Color(value=4246176)
prefix={}

global channel, SESSIONID, latest_tweet_id, roles_allowed, instagram_accounts, twitter_accounts
roles_allowed=[]

latest_tweet_id = 0
channel=0
SESSIONID="48422447086%3AA755vAGRveJn5j%3A14"
Media_present = False
Extended_entites_present = False
old_posts=[]
instagram_accounts=[]
twitter_accounts = []
tweet_ids = []

intents=discord.Intents.default()
intents.members=True
client=commands.Bot(command_prefix=default_prefix, case_insensitive=True,intents=intents)
wit_client = Wit(os.getenv('wit'))
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_key = os.getenv('access_key')
access_secret = os.getenv('access_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

twitter_accounts = list(db["twitter_accounts"])
instagram_accounts=list(db["instagram_accounts"])

def instagram_get(account, not_loop=False):
    global SESSIONID, old_posts
    if type(SESSIONID)==type("hi"):      
      try:
          
          user=InstagramUser(account,sessionid=SESSIONID)
          url=user.posts[0].post_url
          if (not url in old_posts) or not_loop:
              pos=Post(url)
              headers = {
              "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36",
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
    DiscordComponents(client)         #for discord buttons
    channel=client.get_channel(870668217494953984)
    await channel.purge(limit=10000000000000000000)
    mess=await channel.send(embed=discord.Embed(description="Click the reaction X to stop the bot and repeat for reseting the db",color=color_var))
    await mess.add_reaction(emoji.emojize(":cross_mark:"))
    await mess.add_reaction(emoji.emojize(":repeat_button:"))
    instag.start()

@client.event
async def on_member_join(member):  
  print(str(member)+ "joined")
  try:
    description="""
I'm Econbot (I'm only a computer program), created to help you during your stay in our server!

Before I proceed any further, please make sure to review over the following things (they're very important):

> **1.** Make sure you've registered on Devfolio (if not, go to [this link](https://econhacks-bangalore.devfolio.co/) or type **h!devfolio** and I'll send over a link!)
> **2.** Make sure you've read through the <#853856408512626688> and <#853858318242414603> channels. 

Once you're done the above, here are some reminders of how to proceed in the server:

>  - Verify yourself in <#853865432284266496> and introduce yourself in <#853876912640491530>
>  - Pick up roles in <#853858289242210355>
>  - If you are looking for a team, mention your idea or what kind of people are you looking to collaborate with in the <#872705249964613702> channel (make sure you have the "Need a team" role from <#853858289242210355>)
>  - Ask your queries in <#872766197022728232> and an Organizer or Volunteer will get to it ASAP.
>  - Chat in <#867636783173074995> with people in the hackathon.


For a list of commands that I can respond to, type in **h!help** in a bot channel or a DM!
    """
    embed=discord.Embed(title="Welcome to EconHacks Bangalore Discord Server", description=description,color=color_var)
    embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
    await member.send(embed=embed)
  except:
    channel=client.get_channel(870668217494953984)
    await channel.send(embed=discord.Embed(description="Couldnt sent the message to "+str(member),color=color_var))

@client.event
async def on_reaction_add(reaction, user):  
  global twitter_accounts
  if not user.bot:
    if reaction.message.author == client.user and reaction.message.channel == client.get_channel(870668217494953984):
      if reaction.emoji==emoji.emojize(":cross_mark:"):
          sys.exit()
      if reaction.emoji==emoji.emojize(":repeat_button:"):
          twitter_accounts = []
          db["twitter_accounts"] = []
@client.command()
async def link(ctx,chann:discord.TextChannel):
    global channel
    channel=chann.id
    await ctx.message.delete()
    confirm=client.get_channel(channel)
    await confirm.send("Channel set for updates")
@client.command(aliases=['devfolio'])
async def devfo(ctx):
  await ctx.send("You can register at https://econhacks-bangalore.devfolio.co/")
@client.command(aliases=['link-insta'])
async def add_insta(ctx,*, account):
    global instagram_accounts
    await ctx.message.delete()
    embed=instagram_get(account,True)
    if embed!=None:
      await ctx.send(embed=embed)
      instagram_accounts.append(account)
      db["instagram_accounts"] = instagram_accounts
      await ctx.send(embed=discord.Embed(description=account+" added to the list",color=color_var))
    else:
      await ctx.send(embed=discord.Embed(description="This account may not exist or it may be private, please check the spelling.\nAlso check for issues with instagram",color=color_var))
@client.command(aliases=['sess'])
async def set_sessionid(ctx):
  global SESSIONID
  SESSIONID=get_it()
  channel=client.get_channel(870668217494953984)
  await channel.send(embed=discord.Embed(description=str(SESSIONID),color=color_var))

@client.command(aliases=['unlink-insta'])
async def remove_insta(ctx,*,account):
    global instagram_accounts
    await ctx.message.delete()
    instagram_accounts.remove(account)
    db["instagram_accounts"] = instagram_accounts
    await ctx.send(account+" removed from the list")

@client.command(aliases=["unlink-tweet"])
async def remove_tweet(ctx,*,account):
    global twitter_accounts
    await ctx.message.delete()
    twitter_accounts.remove(account)
    print(twitter_accounts)
    db["twitter_accounts"] = twitter_accounts
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
    embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
    embed.add_field(name="Social",value="h!insta to get insta feed\nh!tweet to get twitter feed")
    embed.add_field(name="Events", value="h!hdt to get hackathon dates")
    embed.add_field(name="Questions", value="h!ques to drop your questions and our team will answer")
    embed.add_field(name="Games", value="h!games to play some mini games and gain some points")
    embed.add_field(name="Addtional Queries", value="`ansh@econhacks.org`")
    await ctx.send(embed=embed)

@tasks.loop(minutes=4)
async def instag():
    global channel, old_posts, SESSIONID, tweet_ids, twitter_accounts, instagram_accounts
    print("loop")
    cha = client.get_channel(channel)
    if channel!=0:
    #twitter
        for twitter_account in twitter_accounts:
            new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
            if new_tweets[0].id not in tweet_ids:
                link = "https://twitter.com/{username}/status/{id}".format(username=twitter_account, id = new_tweets[0].id)
                await cha.send(link)
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
    print(twitter_accounts)
    db["twitter_accounts"] = twitter_accounts
    for each in new_tweets:
        link = "https://twitter.com/{username}/status/{id}".format(username=accountname, id = each.id)
        tweet_ids.append(each.id)
    await ctx.send(link)


@client.command(aliases=["tweet"])
async def fetch_tweets(ctx):
    print(db["twitter_accounts"])
    global twitter_accounts, tweet_ids
    if len(twitter_accounts) != 0:
        for twitter_account in twitter_accounts:
            new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
            for each in new_tweets:
                link = "https://twitter.com/{username}/status/{id}".format(username=twitter_account, id = each.id)
                await ctx.send(link)
                tweet_ids.append(each.id)
    else:
      for twitter_account in db["twitter_accounts"]:
          new_tweets = api.user_timeline(screen_name=twitter_account,count=1, tweet_mode="extended")
          print("yes")
          for each in new_tweets:
              link = "https://twitter.com/{username}/status/{id}".format(username=twitter_account, id = each.id)
              await ctx.send(link)
              tweet_ids.append(each.id)

@client.command()
async def teval(ctx,*,text):
  if ctx.guild.id==858234706305482782:
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
    embed.set_thumbnail(url=client.user.avatar_url_as(format="png"))
    embed.set_author(name="EconHacks Bangalore", icon_url="https://media.discordapp.net/attachments/849271520428949517/867430405497421864/logo.png")
    return embed

@client.command(aliases=["q"])
async def ques(ctx, *, question):
    resp = wit_client.message(question)
    try:
        intent = resp["intents"][0]["name"]
        confidence = resp["intents"][0]["confidence"]
        if confidence > 0.90:
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
                embed = ask_embed("Prizes", "There is over 30 lakhs in the prizepool just waiting to be won bu talented people like you!")
                await ctx.send(embed=embed)
            elif intent == "Register":
                embed = ask_embed("How Do I Register", "You can register on Devfolio using this link -  https://econhacks-bangalore.devfolio.co/")
                await ctx.send(embed=embed)
            elif intent == "Sponsor":
                embed = ask_embed("Who Are The Sponsors", "This hackathon has been made possible by amazing sponsors Qoom, Devfolio, Slingshot, EchoAR, Gather,  Replit, Portis, Polygon, Tezos, Celo and Balsmiq")
                await ctx.send(embed=embed)
            elif intent == "Team_or_individual":
                embed = ask_embed("Do We Participate Individually Or In Teams", "You can submit projects in teams of 1-5 peoplegoing solo is cool too! You can bring your friends as a team, or you can find team members at the event on our Discord server.")
                await ctx.send(embed=embed)
            elif intent == "Team_size":
                embed = ask_embed("Size of teams", "You can submit projects in teams of 1-5 people. Most teams aim to have a mix of people with both design and developer skills.")
                await ctx.send(embed=embed)
            elif intent == "What_can_we_build":
                embed = ask_embed("Theme Of The Hackathon", "This is an Economy based hackathon. You can build anything which provides an economic value and helps the struggling citizens of our country.")
                await ctx.send(embed=embed)
            elif intent == "What_is_a_hackathon":
                embed = ask_embed("What Is A Hackathon", "A hackathon is best described as an “invention marathon”. Anyone who has an interest in technology attends a hackathon to learn, build & share their creations over the course of a weekend in a relaxed and welcoming atmosphere. You don’t have to be a programmer and you certainly don’t have to be majoring in Computer Science.")
                await ctx.send(embed=embed)
            elif intent == "Who_can_take_part":
                embed = ask_embed("Who Can Take Part", "All high and middle school students are eligible to participate in this awesome hackathon!")
                await ctx.send(embed=embed)
            elif intent == "Does_it_have_to_be_a_new_project":
              embed = ask_embed("Can we work on it before the hackathon starts", "No, the projects have to be developed during the timeframe and previous worked on projects cannot be submitted.")
              await ctx.send(embed=embed)
            elif intent == "How_to_make_a_team":
              embed = ask_embed("How to create or join a team?", "You can DM others looking for a team on Discord or you can invite your friends to join you!")
              await ctx.send(embed=embed)
            elif intent == "How_to_use_discord":
              embed = ask_embed("How does does discord work", "If you're new to discord, no worries! Check out Wikihow's article (https://www.wikihow.com/Get-Started-with-Discord) and Discord's article (https://support.discord.com/hc/en-us/articles/360045138571-Beginner-s-Guide-to-Discord) and you'll be pretty much set! If you have any more queries, you can ask your fellow server-mates or moderators by making a ticket for guidance.")
              await ctx.send(embed=embed)
            elif intent == "Speakers":
              embed = ask_embed("Workshops", "Gain insights and knowledge from guest speaker series! Our guest speakers have many years of experience in their field of expertise.")
              await ctx.send(embed=embed)
            elif intent == "Speakers":
              embed = ask_embed("Workshops", "Gain insights and knowledge from guest speaker series! Our guest speakers have many years of experience in their field of expertise.")
              await ctx.send(embed=embed)
            elif intent == "What_are_the_rules":
              embed = ask_embed("Rules", """1. Follow Discord's Terms of Service & Community Guidelines at all times.
              Discord ToS  https://discord.com/terms
              Guidelines https://discord.com/guidelines 
              -  Also note that we follow MLH's code of conduct, listed here https://static.mlh.io/docs/mlh-code-of-conduct.pdf

              2. Be mature
              -  Be nice to everyone.
              -  Ping a mod with reason listed in same message if someone appears to be breaking a rule.
              -  Do not cause unnecessary annoyance to anyone.
              -  Don't use any form of derogatory slang/terms / overly offensive language (Direct ban if done on purpose.)
              -  No misusing of exploits or intentional permissions give to you for your convenience. They can be taken from you.

              3. No Advertising
              Do not post or link your socials unless explicitly allowed by a mod except for in the #connect channel. Also, note that the channel cannot have discord server links.
              DMing our users without warning is also against the rules and gets a mute or a ban. 

              4. NO NSFW MATERIAL.
              This includes any form of media deemed to be sexual, gore, or abusive to any lifeform. This rule will get you a direct ban even if you are a regular person on the server.

              5. Don't tag staff for meaningless reasons
              When pinging the moderators (@moderators), make sure that
                -  No staff members are in chat.
                - It requires immediate attention (Raid, Spam, etc... ).
                - Your messages contains the reasoning for the ping,
              (If you would like to report a user, but it isn't of immediate urgency, please do 
              ?report @user reason here.) 

              6. If any rules are broken by you here, expect a punishment whose severity is decided by the mods. Rules 1 and 4 get direct bans, while others may get specific perms removed entirely, or a temporary mute.

              7. If there aren't any rules listed here that tell to explicitly  not do something, it does not mean it is allowed. Use common sense, ask before doing or make a ticket and ask if it is still unclear.
""")
              await ctx.send(embed=embed)
            elif intent == "What_is_Econbot":
              embed = ask_embed("Who am I?", "I'm Econbot, created to help you during your stay in our server! I was made by the wonderfull team of voluteers at econhacks in the Python language.")
              await ctx.send(embed=embed)
            elif intent == "Where_is_the_hackathon_taking_place":
              embed = ask_embed("On which platforms will the hackathon take place?", "The hacakthon will take place over Discord and Gather")
              await ctx.send(embed=embed)
            elif intent == "Who_are_the_organizers":
              embed = ask_embed("Organizers", "This hackathon was organized by 7 passionate high school students who wanted to help solve the economic crisis caused by the pandemic.")
              await ctx.send(embed=embed)
            elif intent == "Who_are_the_organizers":
              embed = ask_embed("Organizers", "This hackathon was organized by 7 passionate high school students who wanted to help solve the economic crisis caused by the pandemic.")
              await ctx.send(embed=embed)
            elif intent == "Who_made_you":
              embed = ask_embed("Organizers", "I was made by the wonderfull team of voluteers at econhacks in the Python language")
              await ctx.send(embed=embed)
            elif intent == "Why_I_exist":
              embed = ask_embed("Meaning of life", "To help make the world a wonderfull place! and to participate in EconHacks Bangalore :joy:")
              await ctx.send(embed=embed)
            elif intent == "website_of_the_hackathon":
              embed = ask_embed("Official website", "Please visit https://econhacksbangalore.live/ for more info.")
              await ctx.send(embed=embed)
            elif intent == "who_are_the_mentors":
              embed = ask_embed("Mentors", "We have two mentors to date. Will update later.")
              await ctx.send(embed=embed)
        else:
        #   question= message.content.replace('h!ques ', '')
            rs = RandomStuff(async_mode=True,api_key=CBAPI)
            res = await rs.get_ai_response(question)
            await ctx.send(res[0]["message"])

            
    except Exception as e:
        print(e)
        rs = RandomStuff(async_mode=True,api_key=CBAPI)
        res = await rs.get_ai_response(question)
        await ctx.send(res[0]["message"])
        # await ctx.send(embed=discord.Embed(description="Oops. Sorry, I didn't get that. Could you please ask the question in the <#872766197022728232> channel and our organizers or volunteers will get back to you as soon as possible.",color=color_var))
        # print(question)

#===============LEVEL================
@client.command()
async def levels(ctx):
    with open('level.json') as f:
        users=json.load(f)
        values = list(users.values())
    new_dict = {}
    for k, v in users.items():
        new_dict.setdefault(v, []).append(k)
    values=list(new_dict.values())
    k=0
    top_users=['```POINTS   PLAYERS```']
    for i in values:
        for j in i:
            k+=1
            if k >15:         #for top 15 users
                break
            top_users.append(f"```{users[j]}       {client.get_user(int(j))}```")
    e1 = discord.Embed(title=" Leaderboard ", description='\n'.join(top_users),color=0x00FF00)
    await ctx.send(embed=e1)
    await ctx.reply(f"```Your points : {users[str(ctx.author.id)]}```")

#===========NEW USER FOR GAME==========
def see(users):
    with open('level.json','w') as fin:
        json.dump(users,fin) 

#================GAMES=================
@client.command()
async def games(ctx):
  Game=['**h!bonk\n**:> play Whac-A-Mole\n !bonk @member\n h!bonk @member @member #for 3 players\n','**h!rps\n**:> play Rock Paper Scissors (2 points)\n','**h!guess\n**:> Can you guess which colour is it ?(1 point)\n','**h!amongus\n**:> shhhhhhhhh!(1 point)\n','**h!football\n**:> Wanna goal ?(2 points)\n','**h!quiz\n**:> Answer Answer Answer whooo...(3 points)\n']
  game=discord.Embed(title='Games', description =''.join(Game),color=0x3498db)
  await ctx.send(embed=game)
  with open('level.json') as f:
    users=json.load(f)
    if str(ctx.author.id) not in users:
        users[str(ctx.author.id)]=1
    see(users)

#=================AMONG US==============
@client.command()
async def amongus(ctx):
    ch=['Blue ඞ','Green ඞ','Red ඞ','grey ඞ']
    comp=random.choice(ch)

    e = discord.Embed(title=f"{ctx.author.name}'s' amongus Game!", description="> Kill the imposter fast! <",color=0x3498db)
    
    e1 = discord.Embed(title=f"{ctx.author.name}, You Guessed It Right!", description="> You have won! <",color=0x00FF00)
    
    e3 = discord.Embed(title=f"{ctx.author.name}, You didn't Click on Time", description="> Timed Out! <",color=discord.Color.red())

    e2 = discord.Embed(title=f"{ctx.author.name}, You Lost!", description=f"> You have lost! < It was {comp}",color=discord.Color.red())

    m = await ctx.reply(
        embed=e,
        components=[[Button(style=1, label="Blue ඞ"),Button(style=3, label="Green ඞ"),Button(style=ButtonStyle.red,label="Red ඞ"),Button(style=ButtonStyle.grey,label="grey ඞ")]
        ],
    )

    def check(res):
      return ctx.author == res.user and res.channel == ctx.channel

    try:
      res = await client.wait_for("button_click", check=check, timeout=5)
      
      if res.component.label==comp:
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=1
                e1.set_footer(text="Your gained 1 point", icon_url=ctx.author.avatar_url)
                await m.edit(embed=e1,components=[],)
            see(users)
      else: 
        await m.edit(embed=e2, components=[],)
    except asyncio.TimeoutError:
      await m.edit(
          embed=e3,
          components=[],
      )

#=============Rock Paper Scissors========
@client.command()
async def rps(ctx):
    ch1 = ["Rock","Scissors","Paper"]
    comp = random.choice(ch1)
  
    yet = discord.Embed(title=f"{ctx.author.display_name}'s ROCK PAPER SCISSORS Game",description=">status: Waiting for a click , 5 sec left" )
    
    win = discord.Embed(title=f"{ctx.author.display_name}, You won!",description=f">status: You Won -- Bot had chosen {comp}")
    
    out = discord.Embed(title=f"{ctx.author.display_name}' You didn't click on time",description=">status: Time Out!!")
    
    lost = discord.Embed(title=f"{ctx.author.display_name}You lost the Game",description=f">status: bot had chosen {comp}")
  
    tie = discord.Embed(title=f"{ctx.author.display_name} Game Tie>",description=">status: It was tie")
    
    
    m = await ctx.reply(
        embed=yet,
        components=[[Button(style=1, label="Rock",emoji="💎"),Button(style=3, label="Paper",emoji="📝"),Button(style=ButtonStyle.red, label="Scissors",emoji="✂️")]
        ],
    )

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
      res = await client.wait_for("button_click", check=check, timeout=7)
      player = res.component.label
      
      if player==comp:
        await m.edit(embed=tie,components=[])
        
      if player=="Rock" and comp=="Paper":
        await m.edit(embed=lost,components=[])
        
      if player=="Rock" and comp=="Scissors":
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)
      
      if player=="Paper" and comp=="Rock":
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)

      if player=="Paper" and comp=="Scissors":
        await m.edit(embed=lost,components=[])
        
        
      if player=="Scissors" and comp=="Rock":
        await m.edit(embed=lost,components=[])
        
      if player=="Scissors" and comp=="Paper":
        with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)

    except asyncio.TimeoutError:
      await m.edit(
          embed=out,
          components=[],
      )

#=========Whac-A-Mole===========
@client.command(aliases=["wam", "whac"])
async def bonk(ctx, member : discord.Member=None, member1 : discord.Member=None):
  await ctx.reply('```By default quit time is 10 sec of inactivity```')
  points = {ctx.author: 0, member: 0,member1: 0}
  random_time = random.randrange(5,25)
  if member == None:
    await ctx.send(f"{ctx.author.mention}, You need to mention a member to play with.")
  if member == client.user:
    await ctx.send(f"{ctx.author.mention}, Hey! Are you trying to catch me??! Mention someone else.")
  if member.bot == True:
    await ctx.send(f"{ctx.author.mention}, You can't play with a bot.")
  else:
    game = True
    try:
      await ctx.send(f"{ctx.author.mention} and {member.mention} and {member1.mention}, I will alert you when a Mole will jump so you can bonk it 🔨")
    except:
      await ctx.send(f"{ctx.author.mention} and {member.mention}, I will alert you when a Mole will jump so you can bonk it 🔨")

    def check(m):
      return m.author.id == member.id or m.author.id == ctx.author.id or m.author.id == member1.id
    while game:
      try:
        await asyncio.sleep(random_time)
        try:
          await ctx.send(f"{ctx.author.mention}, {member.mention}and {member1.mention}, A Mole has jumped! Type `bonk` to bonk it!")
        except:
          await ctx.send(f"{ctx.author.mention} and {member.mention}, A Mole has jumped! Type `bonk` to bonk it!")

        message = await client.wait_for("message", check=check, timeout=15)
        
        if message.author.id == member.id and message.content.lower() == "bonk":
          points[member] += 1
          await ctx.send(f"{member.name} has bonk the mole! They have **{points[member]}** point(s)!")
  
        elif message.author.id == ctx.author.id and message.content.lower() == "bonk":
          points[ctx.author] += 1
          await ctx.send(f"{ctx.author.name} has bonk the mole! They have **{points[ctx.author]}** point(s)!")
        elif message.author.id == member1.id and message.content.lower() == "bonk":
          points[member1] += 1
          await ctx.send(f"{member1.name} has bonk the mole! They have **{points[member1]}** point(s)!")

      except Exception as e:
        game = False
        print(e)
        embed = discord.Embed(
          title = "Game Over",
          description = "No one bonk 🔨 the mole in time so the game is over. Final Scores Below.")
        try:
          embed.add_field(name = f"{member.name}'s score", value = f"{points[member]}")
          embed.add_field(name = f"{member1.name}'s score", value = f"{points[member1]}")
          embed.add_field(name = f"{ctx.author.name}'s score", value = f"{points[ctx.author]}")
        except:
          embed.add_field(name = f"{member.name}'s score", value = f"{points[member]}")
          embed.add_field(name = f"{ctx.author.name}'s score", value = f"{points[ctx.author]}")
        await ctx.send(embed=embed)

#=============Football========
@client.command()
async def football(ctx):
  options=["LEFT",'MIDDLE','RIGHT']
  computerOption = random.choice(options)
  def goal():
    if computerOption=='LEFT':
        return('.🧍‍♂️')
    if computerOption=='MIDDLE':
        return ('⁃⁃⁃⁃⁃⁃⁃🧍‍♂️⁃⁃⁃⁃⁃')
    if computerOption=='RIGHT':
        return ('⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃⁃🧍‍♂️')

  yet = discord.Embed(title=f"{ctx.author.display_name}'s PENALTY SHOOTOUT GAME",description=">status: Waiting for a click , 5 sec left" )
  yet.add_field(name=".🥅    🥅    🥅", value=goal() , inline=False)
  out = discord.Embed(title=f"{ctx.author.display_name}' You didn't click on time",description=">status: Time Out!!")
  win = discord.Embed(title=f"{ctx.author.display_name}, congratulations!",description="GOOOOOAL !!!!")
  miss = discord.Embed(title="MISSED !!",description="Keeper dived")
  save = discord.Embed(title="SAVED !!",description="Keeper saved")

  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel

  m = await ctx.reply(
        embed=yet,
        components=[[Button(style=1, label="LEFT",emoji="⚽"),Button(style=3, label="MIDDLE",emoji="⚽"),Button(style=ButtonStyle.red, label="RIGHT",emoji="⚽")]
        ],
    )
  missChance=random.randint(1,2)
  try:
    res = await client.wait_for("button_click", check=check, timeout=7)
    shoot = res.component.label
    if shoot == computerOption :
      await m.edit(embed=save,components=[])
    elif missChance == 1:
      await m.edit(embed=miss,components=[])
    else :
      with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=2
                win.set_footer(text="Your gained 2 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=win,components=[])
            see(users)

  except asyncio.TimeoutError:
    await m.edit(
          embed=out,
          components=[],
      )
      
#=======GUESS===========
@client.command()
async def guess(ctx):
    ch=['Blue','Green','Red','Grey']
    comp=random.choice(ch)
    
    e = discord.Embed(title=f"{ctx.author.name}'s' Guessing Game!", description="> Click a button to choose! <",color=0x3498db)
    e1 = discord.Embed(title=f"{ctx.author.name}, You Guessed It Right!", description="> You have won! <",color=0x00FF00)
    e3 = discord.Embed(title=f"{ctx.author.name}, You didn't Click on Time", description="> Timed Out! <",color=discord.Color.red())
    e2 = discord.Embed(title=f"{ctx.author.name}, You Lost!", description=f"> You have lost! < It was {comp}",color=discord.Color.red())

    m = await ctx.reply(
        embed=e,
        components=[[Button(style=1, label="Blue"),Button(style=3, label="Green"),Button(style=ButtonStyle.red,label="Red"),Button(style=ButtonStyle.grey,label="Grey")]
        ],
    )
    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel
    try:
        res = await client.wait_for("button_click", check=check, timeout=5)
        if res.component.label==comp:
          with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=1
                e1.set_footer(text="Your gained 1 point", icon_url=ctx.author.avatar_url)
                await m.edit(embed=e1,components=[],)
            see(users)
        else: 
          await m.edit(embed=e2, components=[],)
          
    except asyncio.TimeoutError:
        await m.edit(
            embed=e3,
            components=[],
        )

#================QUIZ==================
@client.command()
async def quiz(ctx):
  e1 = discord.Embed(title=f"{ctx.author.name} , You Guessed It Right!", description="> You have scored! <",color=0x00FF00)
  e2 = discord.Embed(title=f"{ctx.author.name} , You Lost!", description=f"> Try again <",color=discord.Color.red())
  e3 = discord.Embed(title=f"{ctx.author.name}, You didn't Click on Time", description="> Timed Out! <",color=discord.Color.red())

  url='https://opentdb.com/api.php?amount=1&category=18&difficulty=easy&type=multiple'
  response=requests.get(url)
  json_data=json.loads(response.text)
  question=(list(json_data.values())[1][0]["question"])
  p=(list(json_data.values())[1][0]["correct_answer"])
  t=(list(json_data.values())[1][0]["incorrect_answers"])
  t.append(p)
  random.shuffle(t)

  def check(res):
      return ctx.author == res.user and res.channel == ctx.channel

  e = discord.Embed(title=f"{ctx.author.name}'s QUIZ Game!", description=f"**Q) {question}**",color=0x3498db)
  m = await ctx.reply(embed=e,components=[[Button(style=1, label=f"{t[0]}"),Button(style=3, label=f"{t[1]}"),Button(style=ButtonStyle.red,label=f"{t[2]}"),Button(style=ButtonStyle.grey,label=f"{t[3]}")]],)
  try:
    res = await client.wait_for("button_click", check=check, timeout=20)
  except asyncio.TimeoutError:
    await m.edit(embed=e3,components=[],)
    return

  if res.component.label==p:
    with open('level.json') as f:
            users=json.load(f)
            if str(ctx.author.id) not in users:
                users[str(ctx.author.id)]=1
            if str(ctx.author.id) in users:
                users[str(ctx.author.id)]+=3
                e1.set_footer(text="Your gained 3 points", icon_url=ctx.author.avatar_url)
                await m.edit(embed=e1,components=[],)
            see(users)
  else:
    await m.edit(embed=e2,components=[],)
@client.command()
async def econify(ctx, member:discord.Member=None):
    if member is None:
        a=str(ctx.author.avatar_url_as(format="jpg"))
        a=a.strip('?size=1024')
        print(a)
        
        req = requests.get(a).content
        

        arr = np.asarray(bytearray(req), dtype=np.uint8)


        img = cv2.imdecode(arr, -1)
        
        canny = canny_img(img)
        cv2.imwrite('canny.jpg', canny)
        img = cv2.imread('canny.jpg')
        b, g, r = cv2.split(img) 
        blank = np.zeros(img.shape[:2], dtype='uint8')

        green = cv2.merge([blank,g,blank])
        green = cv2.cvtColor(green, cv2.COLOR_BGR2RGB)
        a=cv2.imwrite('green.jpg', green)
        
        file=discord.File("green.jpg")
        
        embed = discord.Embed(title="Profile Picture : {}".format(ctx.author.name), color=color)
        embed.set_image(url="attachment://green.jpg")
        
    else:
        a=str(member.avatar_url)
        req = requests.get(a).content
        

        arr = np.asarray(bytearray(req), dtype=np.uint8)


        img = cv2.imdecode(arr, -1)


        canny = canny_img(img)
        cv2.imwrite('canny.jpg', canny)
        img = cv2.imread('canny.jpg')
        b, g, r = cv2.split(img) 
        blank = np.zeros(img.shape[:2], dtype='uint8')

        green = cv2.merge([blank,g,blank])
        
        green = cv2.cvtColor(green, cv2.COLOR_BGR2RGB)
        a=cv2.imwrite('green.jpg', green)
        file=discord.File("green.jpg")
        
        embed = discord.Embed(title="Profile Picture : {}".format(member.name), color=color)
        embed.set_image(url='attachment://green.jpg')
        
    await ctx.send(file=file, embed=embed)
client.run(os.getenv('token'))
