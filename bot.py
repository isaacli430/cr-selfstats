'''
MIT License

Copyright (c) 2017 kwugfighter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import discord
from discord.ext import commands
from formatter import EmbedHelp
import os
import asyncio
import json
import aiohttp

def run_setup():
    print("Let's set up the bot now:\n")
    token = input("Enter your token here\n>")
    prefix = input('Enter yout prefix here (If nothing is entered it will be set to "st.")\n>')
    profile_id = input("Enter your Clash Royale profile ID here (DO NOT LEAVE THIS BLANK)\n>")
    if prefix == "":
        prefix == "st."
    while profile_id == "":
        profile_id = input("Enter your Clash Royale profile ID here (DO NOT LEAVE THIS BLANK)\n>")
    config_data = {
        "TOKEN" : token,
        "PREFIX" : prefix,
        "PROFILE_ID" : profile_id
        }
    with open("data/config.json", "w") as f:
        f.write(json.dumps(config_data, indent=4))

if "TOKEN" in os.eviron:
    token = os.environ["TOKEN"]
    heroku = True
else:
    with open("data/config.json") as f:
        config = json.load(f)
        if config.get('TOKEN') == "token" or "":
            run_setup()
        else:
            token = config.get('TOKEN').strip('\"')
            heroku = False

if heroku == True:
    profile_id = os.environ['PROFILE_ID']
else:
    with open("data/config.json") as f:
        profile_id = json.load(f).get('PROFILE_ID')

async def prefix(bot, message):
    global heroku
    if heroku == True:
        return os.environ["PREFIX"] or "st."
    else:
        with open("data/config.json") as f:
            return json.load(f).get('PREFIX') or "st."

bot = commands.Bot(command_prefix=prefix, self_bot=True, formatter=EmbedHelp())

@bot.event
async def on_ready():
    print("Bot has booted up!\nCreator: kwugfighter")

@bot.command(aliases=['stats', 'p', 's'])
async def profile(ctx, tag=profile_id):
    tag = tag.replace("#", "")
    if tag == None:
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="Please add PLAYER_ID to your config vars in Heroku.")
        return await ctx.send(embed=em)
    url = f"http://api.cr-api.com/profile/{tag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as d:
            data = await d.json()
    if data.get("error"):
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="That's an invalid Player ID.")
        return await ctx.send(embed=em)
    em = discord.Embed(color=discord.Color(value=0x33ff30), title=data['name'], description=f"#{data['tag']}")
    em.set_author(name="Profile", url=f"http://cr-api.com/profile/{tag}", icon_url=f"http://api.cr-api.com{data['clan']['badgeUrl']}")
    em.set_thumbnail(url=f"http://api.cr-api.com{data['arena']['imageURL']}")
    if data['experience']['xpRequiredForLevelUp'] == "Max":
        to_level_up = "(Max Level)"
    else:
        to_level_up = f"({data['experience']['xp']}/{data['experience']['xpRequiredForLevelUp']})"
    em.add_field(name="Level", value=f"{data['experience']['level']} {to_level_up}", inline=True)
    em.add_field(name="Arena", value=data['arena']['name'], inline=True)
    em.add_field(name="Clan Info", value=f"**{data['clan']['name']} (#{data['clan']['tag']})**\n{data['clan']['role']}", inline=True)
    em.add_field(name="Favorite Card", value=data['stats']['favoriteCard'].replace('_', ' ').title())
    deck = f"**{data['currentDeck'][0]['name'].replace('_', ' ').title()}** - Lvl {data['currentDeck'][0]['level']}"
    for i in range(1,8):
        deck += f"\n**{data['currentDeck'][i]['name'].replace('_', ' ').title()}** - Lvl {data['currentDeck'][i]['level']}"
    em.add_field(name="Deck", value=deck)

    em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    await ctx.send(embed=em)

try:
    bot.run(token.strip('\"'), bot=False)
except Exception as e:
    print("Your token is invalid, please edit your token in the configs.")