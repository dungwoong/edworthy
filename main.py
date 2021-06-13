"""
This is the main discord bot code.
"""

import json

import discord
from discord.ext import commands, tasks
import LocationGetter
from statistics import mean
import datetime

# https://python.plainenglish.io/send-an-embed-with-a-discord-bot-in-python-61d34c711046
# https://stackoverflow.com/questions/57631314/making-a-bot-that-sends-messages-at-a-scheduled-date-with-discord-py
URL = 'https://www.google.com/search?q='
EDWORTHY = 'edworthy+park'
BOWNESS = 'bowness+park'
NOSEHILL = 'nose+hill+park'
PRINCESISLAND = 'prince%27s+island+park'
DAMASCUS = 'damascus+calgary'
LOCATIONDICT = {'Edworthy': EDWORTHY,
                'Bowness': BOWNESS,
                'Nose Hill': NOSEHILL,
                "Prince's island": PRINCESISLAND,
                "Damascus": DAMASCUS}
config_file = 'config.json'


def get_config():
    with open(config_file, 'r') as file:
        config = json.load(file)
        return config


cfg = get_config()
TOKEN = cfg['token']

bot = commands.Bot(command_prefix='?', help_command=None)


# client = discord.Client()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord')
    check_good_loc.start()
    collect_info.start()
    game = discord.Game("?help")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=game)


@bot.command(name='test')
async def basic_command(ctx):
    msg = '*nice* #### {0.author.mention}'.format(ctx.message)
    await ctx.send(msg)


@bot.command(name='embed_demo')
async def embed_demo(ctx):
    embed = discord.Embed(title="Title", description="DESC", color=0xff0000)
    embed.add_field(name='field1', value="FIELD1", inline=False)
    embed.add_field(name='field2', value="FIELD2", inline=False)
    # embed.set_author(name='AUTHOR')
    await ctx.send(embed=embed)


# ACTUALLY USEFUL SHIT
@bot.command(name='help')
async def help_command(ctx):
    desc = 'test: testing command\n' \
           'embed_demo: embed demo command\n' \
           'park: park info\n' \
           'notif: notify if anything good'
    embed = discord.Embed(title="Info", description=desc, color=0xb0605d)
    await ctx.send(embed=embed)


@bot.command(name='park')
async def location_info(ctx):
    """NOTES:
    - Avg popularity for the day excludes 0 values
    - Max popularity is 0.75 I think
    """
    await ctx.send('Getting info for {0.author.mention}:'.format(ctx.message))
    # print('{0.author.mention}'.format(ctx.message))
    desc = "Max occupancy is 100."
    embed = discord.Embed(title="Info", description=desc, color=0xb0605d)
    for location in LOCATIONDICT:
        # I want to report current/usual bars, then the max bar for today.
        locdic, loclst = LocationGetter.get_bar_height(LOCATIONDICT[location])
        loclst = [i for i in loclst if i != 0]
        info = ''
        if 'Usual' in locdic and 'Current' in locdic:
            info += f"**[{round(100 * locdic['Current'] / locdic['Usual'])}% / {locdic['Current']}]**\n\n"
            info += f"Usual/Current = [{locdic['Usual']}/{locdic['Current']}]\n"
        else:
            info += "Could not compute stats.\n\n"
        if 'Unknown' in locdic:
            info += f"Unknown: {locdic['Unknown']}\n"
        # info += f'Daily Max: {max(loclst)}'
        info += f'Avg Popularity for the day: {round(mean(loclst))}'
        embed.add_field(name=location, value=info, inline=False)
    await ctx.send(embed=embed)


@bot.command(name='notif')
async def notif_loc(ctx):
    embed = discord.Embed(title="Info", description='', color=0xb0605d)
    report = ''
    for location in LOCATIONDICT:
        locdic, _ = LocationGetter.get_bar_height(LOCATIONDICT[location])
        if 'Usual' in locdic and 'Current' in locdic:
            report = check_uc(locdic['Usual'], locdic['Current'])
        if report == '':
            embed.add_field(name=location, value='*Nothing*', inline=False)
        else:
            embed.add_field(name=location, value=report, inline=False)
    await ctx.send(embed=embed)


# HELPERS
def check_uc(u: float, c: float) -> str:
    """Checks for abnormal things."""
    ret_str = ''
    max_occ = 100
    if c / u <= 0.6:
        ret_str += f'Current occupancy at {round(100 * c / u)}% of usual!\n'
    if c / max_occ <= 0.4:
        ret_str += f'Current occupancy is {c}/{max_occ}!\n'
    return ret_str


@tasks.loop(hours=1)
async def check_good_loc():
    print('Hourly notif')
    # This is really hard to test, but I think it works. Check the notif command, it's similar to this.
    uid = 231241995253710851
    # OH FUCK IT WORKS OK
    channel = await bot.fetch_user(uid)
    if channel is None:
        return
    now = datetime.datetime.now()
    if now.hour < 12 or now.hour > 20:
        # Don't do any checks, just stop lol
        return
    should_send = False
    embed = discord.Embed(title="HOURLY UPDATE", description='', color=0xb0605d)
    report = ''
    for location in LOCATIONDICT:
        locdic, _ = LocationGetter.get_bar_height(LOCATIONDICT[location])
        if 'Usual' in locdic and 'Current' in locdic:
            report = check_uc(locdic['Usual'], locdic['Current'])
        if report == '':
            embed.add_field(name=location, value='*Nothing*', inline=False)
        else:
            embed.add_field(name=location, value=report, inline=False)
            should_send = True
    if should_send:
        await channel.send(embed=embed)


@tasks.loop(hours=1)
async def collect_info():
    now = datetime.datetime.now()
    # hour is 0-23
    # Monday = 0, sunday = 6
    if now.hour < 6 or now.hour > 21:
        # Don't do any checks, just stop lol
        return
    locdic, _ = LocationGetter.get_bar_height(EDWORTHY)
    if 'Usual' in locdic and 'Current' in locdic:
        LocationGetter.write_dict(locdic)


bot.run(TOKEN)
