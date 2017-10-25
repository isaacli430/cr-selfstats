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
from PIL import Image
import os
import asyncio
import json
import aiohttp
import embedtobox
import io

def run_setup():
    print("Let's set up the bot now:\n")
    token = input("Enter your token here (DO NOT LEAVE THIS BLANK)\n>")
    while token == "":
        token = input("Enter your token here (DO NOT LEAVE THIS BLANK)\n>")
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

if "TOKEN" in os.environ:
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

if "PROFILE_ID" in os.environ:
    profile_id = os.environ['PROFILE_ID']
else:
    with open("data/config.json") as f:
        profile_id = json.load(f).get('PROFILE_ID')

def prefix(bot, message):
    if heroku == True:
        return os.environ["PREFIX"] or "st."
    else:
        with open("data/config.json") as f:
            return json.load(f).get('PREFIX') or "st."

if heroku == True:
    current_prefix =  os.environ["PREFIX"] or "st."
else:
    with open("data/config.json") as f:
        current_prefix = json.load(f).get('PREFIX') or "st."


bot = commands.Bot(command_prefix=prefix, self_bot=True)
bot.remove_command("help")

@bot.event
async def on_ready():
    global current_prefix
    print(f"---------------\nBot has booted up!\nCreator: kwugfighter\n---------------\nDo {current_prefix}help to get a list of commands\n--------------")


@bot.command()
async def help(ctx, command=None):
    '''Shows this message.'''
    em = discord.Embed(color=0x33ff30)
    if command == None:
        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        em.title = "``Help``"
        em.description = f"Type `{ctx.prefix}help command` for more info on a command."
        for command in bot.commands:
            if command.short_doc == "":
                short_doc = "No Description"
            else:
                short_doc = command.short_doc
            em.add_field(name=f"{ctx.prefix}{command.name}", value=short_doc, inline=False)
            em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    else:
        command = discord.utils.find(lambda c: command.lower() in c.name.lower(), bot.commands)
        if command == None:
            em.title = "Command Help"
            em.description = "That command doesn't exist."
            return await ctx.send(embed=em)
        params = list(filter(lambda a: a != 'ctx', list(command.params)))
        param_str = f"``Usage:`` `{ctx.prefix}{command.name} "
        for param in params:
            param_str += f"<{param}> "
        param_str += "`"
        em.title = param_str
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)

@bot.command()
async def presence(ctx, status, *, message=None):
    '''Change your Discord status! (Stream, Online, Idle, DND, Invisible, or clear it).'''
    status = status.lower()
    emb = discord.Embed(title="Presence", color=discord.Color(value=0x33ff30))
    file = io.BytesIO()
    if status == "online":
        await bot.change_presence(status=discord.Status.online, game=discord.Game(name=message), afk=True)
        color = discord.Color(value=0x43b581).to_rgb()
    elif status == "idle":
        await bot.change_presence(status=discord.Status.idle, game=discord.Game(name=message), afk=True)
        color = discord.Color(value=0xfaa61a).to_rgb()
    elif status == "dnd":
        await bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=message), afk=True)
        color = discord.Color(value=0xf04747).to_rgb()
    elif status == "invis" or status == "invisible":
        await bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=message), afk=True)
        color = discord.Color(value=0x747f8d).to_rgb()
    elif status == "stream":
        await bot.change_presence(status=discord.Status.online, game=discord.Game(name=message,type=1,url=f'https://www.twitch.tv/{message}'), afk=True)
        color = discord.Color(value=0x593695).to_rgb()
    elif status == "clear":
        await bot.change_presence(game=None, afk=True)
        emb.description = "Presence cleared."
        return await ctx.send(embed=emb)
    else:
        emb.description = "Please enter either `stream`, `online`, `idle`, `dnd`, `invisible`, or `clear`."
        return await ctx.send(embed=emb)

    Image.new('RGB', (500, 500), color).save(file, format='PNG')
    emb.description = "Your presence has been changed."
    file.seek(0)
    emb.set_author(name=status.title(), icon_url="attachment://color.png")
    emb.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    try:
        await ctx.send(file=discord.File(file, 'color.png'), embed=emb)
    except discord.HTTPException:
        em_list = await embedtobox.etb(emb)
        for page in em_list:
            await ctx.send(page)

@bot.command(aliases=['cl'])
async def clan(ctx, tag=profile_id, tag_type="clan"):
    '''Returns the stats of a clan.'''
    global profile_id
    if tag == profile_id:
        tag_type = "player"
    tag = tag.replace("#", "")
    if tag == "":
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Please add **PLAYER_ID** to your config vars in Heroku.")
        return await ctx.send(embed=em)
    if tag_type == "player":
        url = f"http://api.cr-api.com/profile/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as d:
                data = await d.json()
        if data.get("error"):
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Player ID.")
            return await ctx.send(embed=em)
        if data['clan'] == None:
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Player is not in a clan.")
            return await ctx.send(embed=em)
        tag = data['clan']['tag']
        url = f"http://api.cr-api.com/clan/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as d:
                data = await d.json()
    elif tag_type == "clan":
        url = f"http://api.cr-api.com/clan/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as d:
                data = await d.json()      
        if data.get("error"):
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Clan ID.")
            return await ctx.send(embed=em) 
    else:
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Please only enter `player` for the tag type if necessary.")
        return await ctx.send(embed=em)

    em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description=f"{data['description']}")
    em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
    em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
    em.add_field(name="Trophies", value=str(data['score']), inline=True)
    em.add_field(name="Type", value=data['typeName'], inline=True)
    em.add_field(name="Member Count", value=f"{data['memberCount']}/50", inline=True)
    em.add_field(name="Requirement", value=str(data['requiredScore']), inline=True)
    em.add_field(name="Donations", value=str(data['donations']), inline=True)
    em.add_field(name="Region", value=data['region']['name'])
    players = []
    for i in range(len(data['members'])):
        if i <= 2:
            players.append(f"{data['members'][i]['name']}: {data['members'][i]['trophies']}\n(#{data['members'][i]['tag']})")
    em.add_field(name="Top 3 Players", value="\n\n".join(players), inline=True)
    contributors = sorted(data['members'], key=lambda x: x['clanChestCrowns'])
    contributors = list(reversed(contributors))
    players = []
    for i in range(len(data['members'])):
        if i <= 2:
            players.append(f"{contributors[i]['name']}: {contributors[i]['clanChestCrowns']}\n(#{contributors[i]['tag']})")
    em.add_field(name="Top CC Contributors", value='\n\n'.join(players), inline=True)
    em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)


@bot.command(aliases=['stats', 'p', 's'])
async def profile(ctx, tag=profile_id):
    '''Returns the stats of a player.'''
    tag = tag.replace("#", "")
    if tag == "":
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="Please add **PLAYER_ID** to your config vars in Heroku.")
        return await ctx.send(embed=em)
    url = f"http://api.cr-api.com/profile/{tag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as d:
            data = await d.json()
    if data.get("error"):
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="That's an invalid Player ID.")
        return await ctx.send(embed=em)
    em = discord.Embed(color=discord.Color(value=0x33ff30), title=data['name'], description=f"#{data['tag']}")
    try:
        em.set_author(name="Profile", url=f"http://cr-api.com/profile/{tag}", icon_url=f"http://api.cr-api.com{data['clan']['badge']['url']}")
    except:
        em.set_author(name="Profile", url=f"http://cr-api.com/profile/{tag}", icon_url=f"https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/clanless.png")
    em.set_thumbnail(url=f"http://api.cr-api.com{data['arena']['imageURL']}")
    if data['experience']['xpRequiredForLevelUp'] == "Max":
        to_level_up = "(Max Level)"
    else:
        to_level_up = f"({data['experience']['xp']}/{data['experience']['xpRequiredForLevelUp']})"
    em.add_field(name="Trophies", value=str(data['trophies']), inline=True)
    em.add_field(name="Personal Best", value=str(data['stats']['maxTrophies']), inline=True)
    em.add_field(name="Level", value=f"{data['experience']['level']} {to_level_up}", inline=True)
    if data['globalRank'] == None:
        global_ranking = "N/A"
    else:
        global_ranking = data['globalRank']
    em.add_field(name="Global Rank", value=global_ranking)
    try:
        em.add_field(name="Total Donations", value=str(data['stats']['totalDonations']), inline=True)
    except:
        em.add_field(name="Total Donations", value="N/A"), inline=True)
    em.add_field(name="Win-Loss", value=f"{round(data['games']['wins']/(data['games']['wins']+data['games']['losses'])*100, 2)}%", inline=True)
    em.add_field(name="Legendary Trophies", value=str(data['stats']['legendaryTrophies']), inline=True)
    em.add_field(name="Max Challenge Wins", value=str(data['stats']['challengeMaxWins']), inline=True)
    em.add_field(name="Arena", value=data['arena']['name'], inline=True)
    em.add_field(name="Favorite Card", value=data['stats']['favoriteCard'].replace('_', ' ').title(), inline=True)
    em.add_field(name="Wins", value=str(data['games']['wins']), inline=True)
    em.add_field(name="Losses", value=str(data['games']['losses']), inline=True)
    em.add_field(name="Draws", value=str(data['games']['draws']), inline=True)
    try:
        em.add_field(name="Clan Info", value=f"{data['clan']['name']}\n(#{data['clan']['tag']})\n{data['clan']['role']}", inline=True)
    except:
        em.add_field(name="Clan Info", value=f"N/A", inline=True)

    try:
        if data['previousSeasons'][0]['seasonEndGlobalRank'] == None:
            ranking = "N/A"
        else:
            ranking = data['previousSeasons'][0]['seasonEndGlobalRank'] + "trophies"
        em.add_field(name="Season Results", value=f"Season Finish: {data['previousSeasons'][0]['seasonEnding']}\nSeason Highest: {data['previousSeasons'][0]['seasonHighest']}\nGlobal Rank: {ranking}", inline=True)
    except:
        em.add_field(name="Season Results", value=f"Season Finish: N/A\nSeason Highest: N/A\nGlobal Rank: N/A", inline=True)
    try:
        supermag = data['chestCycle']['superMagicalPos']-data['chestCycle']['position']+1
    except:
        supermag = "N/A"
    try:
        leggie = data['chestCycle']['legendaryPos']-data['chestCycle']['position']+1
    except:
        leggie = "N/A"
    try:
        epic = data['chestCycle']['epicPos']-data['chestCycle']['position']+1
    except:
        epic = "N/A"
    em.add_field(name="Upcoming Chests", value=f"Super Magical: {supermag}\nLegendary: {leggie}\nEpic: {epic}", inline=True)
    deck = f"{data['currentDeck'][0]['name'].replace('_', ' ').title()}: Lvl {data['currentDeck'][0]['level']}"
    for i in range(1,len(data['currentDeck'])):
        deck += f"\n{data['currentDeck'][i]['name'].replace('_', ' ').title()}: Lvl {data['currentDeck'][i]['level']}"
    em.add_field(name="Battle Deck", value=deck, inline=True)
    offers = ""
    if data['shopOffers']['legendary'] > 0:
        offers += f"Legendary Chest: {data['shopOffers']['legendary']} days\n"
    if data['shopOffers']['epic'] > 0:
        offers += f"Epic Chest: {data['shopOffers']['epic']} days\n"
    if data['shopOffers']['arena'] != None:
        offers += f"Arena Pack: {data['shopOffers']['arena']} days"
    if offers == "":
        offers = "None"
    em.add_field(name="Shop Offers", value=offers, inline=True)

    em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)

@bot.command(aliases=['m'])
async def members(ctx, tag=profile_id, tag_type="clan"):
    '''Returns the members of a clan.'''
    global profile_id
    if tag == profile_id:
        tag_type = "player"
    tag = tag.replace("#", "")
    if tag == "":
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Please add **PLAYER_ID** to your config vars in Heroku.")
        return await ctx.send(embed=em)
    if tag_type == "player":
        url = f"http://api.cr-api.com/profile/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as d:
                data = await d.json()
        if data.get("error"):
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Player ID.")
            return await ctx.send(embed=em)
        if data['clan'] == None:
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Player is not in a clan.")
            return await ctx.send(embed=em)
        tag = data['clan']['tag']
        url = f"http://api.cr-api.com/clan/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as d:
                data = await d.json()
    elif tag_type == "clan":
        url = f"http://api.cr-api.com/clan/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as d:
                data = await d.json()      
        if data.get("error"):
            em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Invalid Clan ID.")
            return await ctx.send(embed=em) 
    else:
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Clan", description="Please only enter `player` for the tag type if necessary.")
        return await ctx.send(embed=em)
    em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description='Page 1')
    em.set_author(name="Clan", url=f"http://cr-api.com/clan/{tag}", icon_url=f"http://api.cr-api.com{data['badge']['url']}")
    em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
    for player in data['members']:
        if player['currentRank'] == 26:
            em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
            try:
                await ctx.send(embed=em)
            except discord.Forbidden:
                pages = await embedtobox.etb(em)
                for page in pages:
                    await ctx.send(page)
            em = discord.Embed(color=discord.Color(value=0x33ff30), title=f"{data['name']} (#{tag})", description='Page 2')
            em.set_thumbnail(url=f"http://api.cr-api.com{data['badge']['url']}")
        em.add_field(name=player['name'], value=f"(#{player['tag']})\nTrophies: {player['score']}\nDonations: {player['donations']}\nCrowns: {player['clanChestCrowns']}\nRole: {player['roleName']}")
    em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)

@bot.command(aliases=['ch'])
async def chests(ctx, tag=profile_id):
    '''Get a mini version of a player's chest cycle.'''
    tag = tag.replace("#", "")
    if tag == "":
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="Please add **PLAYER_ID** to your config vars in Heroku.")
        return await ctx.send(embed=em)
    url = f"http://api.cr-api.com/profile/{tag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as d:
            data = await d.json()
    if data.get("error"):
        em = discord.Embed(color=discord.Color(value=0x33ff30), title="Profile", description="That's an invalid Player ID.")
        return await ctx.send(embed=em)
    em = discord.Embed(color=discord.Color(value=0x33ff30), title=data['name'], description=f"#{data['tag']}")
    try:
        em.set_author(name="Chest Cycle", url=f"http://cr-api.com/profile/{tag}", icon_url=f"http://api.cr-api.com{data['clan']['badge']['url']}")
    except:
        em.set_author(name="Chest Cycle", url=f"http://cr-api.com/profile/{tag}", icon_url=f"https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/clanless.png")
    with open('data/chests.json') as c:
        chest = json.load(c)
    cycle_pos = data['chestCycle']['position']%len(chest)
    chest_list = [chest[x] for x in range(cycle_pos, cycle_pos+30)]
    if len(chest_list) != 30:
        chest_listp2 = [chest[x] for x in range(10-len(chest_list))]
        chest_list += chest_listp2
    try:
        supermag = data['chestCycle']['superMagicalPos']-data['chestCycle']['position']+1
    except:
        supermag = "N/A"
    try:
        leggie = data['chestCycle']['legendaryPos']-data['chestCycle']['position']+1
    except:
        leggie = "N/A"
    try:
        epic = data['chestCycle']['epicPos']-data['chestCycle']['position']+1
    except:
        epic = "N/A"
    try:
        chest_list[supermag-1] = "Super Magical"
    except:
        pass
    try:
        chest_list[leggie-1] = "Legendary"
    except:
        pass
    try:
        chest_list[epic-1] = "Epic"
    except:
        pass

    em.add_field(name="Chest Cycle", value="\n".join(chest_list))
    em.add_field(name="Special Chests", value=f"Super Magical: {supermag}\nLegendary: {leggie}\nEpic: {epic}")
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)

@bot.command(aliases=['card'])
async def cardinfo(ctx, *, card : str):
    '''Return a card's info'''
    em = discord.Embed(color=0x33ff30)
    card = card.replace(' ', '-').lower()
    if card == "elixir-pump" or card == "pump":
        card = 'elixir-collector'
    if card == "log":
        card = 'the-log'
    if card == 'x-bow':
        card = 'xbow'
    with open('data/cards.json') as c:
        cardj = json.load(c)
    found_card = None
    for test_card in cardj['cards']:
        if card == test_card['key']:
            found_card = test_card
    if found_card == None:
        em.title = "Card Info"
        em.description = "This card does not exist, please try again."
        return await ctx.send(embed=em)
    em.set_author(name="Card Info", icon_url=f"https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/card_ui/{found_card['key']}.png")
    em.title = found_card['name']
    em.set_thumbnail(url=f"https://raw.githubusercontent.com/kwugfighter/cr-selfstats/master/data/cards/{found_card['key']}.png")
    em.description = found_card['description']
    em.add_field(name="Rarity", value=found_card['rarity'])
    if found_card['arena'] == 0:
        arena = 'Training Camp'
    else:
        arena = f"Arena {found_card['arena']}"
    em.add_field(name="Found In", value=arena)
    em.add_field(name="Card Type", value=found_card['type'])
    em.add_field(name="Elixir Cost", value=found_card['elixir'])
    em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)

@bot.command(aliases=['deck'])
async def sharedeck(ctx, *, deck: str):
    '''Share a deck through URL! Make sure you split up each card with `|`'''
    em = discord.Embed(color=0x33ff30)
    deck = deck.split("|")
    deck = [card.strip() for card in deck]
    with open('data/cards.json') as c:
        cardj = json.load(c)
    new_deck = []
    for card in deck:
        found_card = False
        card = card.replace(' ', '-').lower()
        if card == "elixir-pump" or card == "pump":
            card = 'elixir-collector'
        if card == "log":
            card = 'the-log'
        if card == 'x-bow':
            card = 'xbow'
        for test_card in cardj['cards']:
            if card == test_card['key']:
                new_deck.append(test_card)
                found_card = True
        if not found_card:
            em.title = 'Share a Deck!'
            em.description = 'One of your cards does not exist.'
            return await ctx.send(embed=em)
    try:
        url = f"https://link.clashroyale.com/deck/en?deck={new_deck[0]['decklink']};{new_deck[1]['decklink']};{new_deck[2]['decklink']};{new_deck[3]['decklink']};{new_deck[4]['decklink']};{new_deck[5]['decklink']};{new_deck[6]['decklink']};{new_deck[7]['decklink']}&id=iOS"
        em.url = url
    except:
        em.title = 'Share a Deck!'
        em.description = "You need to have 8 cards in your deck."
        return await ctx.send(embed=em)
    em.description = ', '.join([card['name'] for card in new_deck])
    em.title = 'Click Here to Copy Deck'
    em.set_author(name="Share a Deck!", icon_url=ctx.author.avatar_url)
    em.set_footer(text="Selfbot made by kwugfighter | Powered by cr-api", icon_url="http://cr-api.com/static/img/branding/cr-api-logo.png")
    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)


@bot.event
async def on_command_error(ctx, exception):
    print(exception)
    command = ctx.command or ctx.invoked_subcommand
    em = discord.Embed(color=0x33ff30)

    params = list(filter(lambda a: a != 'ctx', list(command.params)))
    param_str = f"``Usage:`` `{ctx.prefix}{command.name} "
    for param in params:
        param_str += f"<{param}> "
    param_str += "`"
    em.title = param_str

    try:
        await ctx.send(embed=em)
    except discord.Forbidden:
        pages = await embedtobox.etb(em)
        for page in pages:
            await ctx.send(page)
try:
    bot.run(token.replace('"', ''), bot=False)
except Exception as e:
    print("Your token is invalid, please edit your token in the configs.")
