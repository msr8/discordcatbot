from   rich        import print as printf
from   discord.ext import commands
import discord

from   funcs import get_ts, logme
import bot_commands

import json











# Loads the config
with open('config.json') as f:
    config:dict = json.load(f)
# Loads the facts
with open('DATA/facts.json') as f:
    facts:list = json.load(f)
# Loads the help texts
with open('DATA/help.json') as f:
    help_dict:list = json.load(f)
# Loads the ascii cats
with open('DATA/cats.txt') as f:
    ascii_cats = f.read().split('\n\n\n\n\n\n')
# Loads the neofetch text
with open('DATA/neofetch.txt') as f:
    nfetch = f.read()



intents = discord.Intents.default()
bot     = commands.Bot(guild_ids=[1028742298563002490, 1029927181327007815], intents=intents)






@bot.event
async def on_connect():
    logme(f'[grey50][{get_ts()}][/] [b green1]BOT IS UP![/]\n')
    if bot.auto_sync_commands:
        await bot.sync_commands()


@bot.event
async def on_disconnect():
    logme(f'[grey50][{get_ts()}][/] [b red1]BOT IS DOWN :([/]')


@bot.event
async def on_guild_join(guild:discord.Guild):
    # Gets the bot owner
    owner   = (await bot.application_info()).owner
    # Gets the guild owner
    g_owner = await bot.fetch_user( guild.owner_id )
    # Logs it
    await owner.send(f'{g_owner.mention} just added me to **{guild}**!')
    logme(f'\n[grey50][{get_ts()}][/] [b green1]{g_owner} JUST ADDED ME TO {guild}!![/]\n')


@bot.event
async def on_guild_remove(guild:discord.Guild):
    # Gets the bot owner
    owner   = (await bot.application_info()).owner
    # Gets the guild owner
    g_owner = await bot.fetch_user( guild.owner_id )
    # Logs it
    await owner.send(f'{g_owner.mention} just removed me from **{guild}** :(')
    logme(f'\n[grey50][{get_ts()}][/] [b red1]{g_owner} JUST REMOVED ME FROM {guild} :([/]\n')


@bot.event
async def on_application_command_completion(ctx:discord.ApplicationContext):
    # In case the command is called in a DM
    guild = ctx.guild if ctx.guild else f'DM'
    logme(f'[grey50][{get_ts()}][/] [b blue3]{guild}[/] -- [light_steel_blue]{ctx.author}[/] -- [magenta1]/{ctx.command.name}[/]')











@bot.slash_command(name='about', description=help_dict['about'])
@discord.option(name='style', choices=['Embed', 'Neofetch'], default='Embed', description='Display the information in an embed for a neofetch style code block')
async def _(ctx, style:str):
    await bot_commands.about(ctx, bot, style, nfetch, facts, config['eyebleach_path'], config['bot_invite'], config['server_invite'])


@bot.slash_command(name='cat', description=help_dict['cat'])
@discord.option(name='type', choices=['Picture', 'Video'], default='')
async def _(ctx, type:str):
    await bot_commands.cat(ctx, type, config['eyebleach_path'], ascii_cats)


@bot.slash_command(name='fact', description=help_dict['fact'])
async def _(ctx):
    await bot_commands.fact(ctx, facts)


@bot.slash_command(name='invite', description=help_dict['invite'])
async def _(ctx):
    await bot_commands.invite(ctx, config['bot_invite'])


@bot.slash_command(name='help', description='Shows all the bot\'s commands')
async def _(ctx):
    await bot_commands.help(ctx, bot, help_dict)



















bot.run(config['token'])








'''
-> Test joining and leaving of servers

'''

