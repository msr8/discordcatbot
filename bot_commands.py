from discord              import Colour, Embed, File
from discord.ui           import View, Button
from discord.commands     import ApplicationContext
from discord.ext.commands import Bot

from funcs import get_file_path

import random as r
import os






class MyView(View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, bot_inv:str, server_inv:str):
        super().__init__()

        self.add_item(Button(label='Bot Invite',      url=bot_inv))
        self.add_item(Button(label='[WIP] Website',   url='https://apiofcats.xyz'))
        self.add_item(Button(label='Source Code',     url='https://github.com/msr8/discordcatbot'))
        self.add_item(Button(label='Support Server',  url=server_inv))


class InvView(View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, bot_inv:str):
        super().__init__()
        self.add_item(Button(label='Invite',          url=bot_inv))






# async def ping(ctx:ApplicationContext, bot:Bot):
#     latency = int(bot.latency*1000)
#     await ctx.respond(f'My latency is {latency}ms')







async def about(ctx:ApplicationContext, bot:Bot, style:str, nfetch:str, facts:list, eyebleach_path:str, bot_inv:str, server_inv:str):
    msg = await ctx.respond('```\nCalculating...```')

    view     = MyView(bot_inv, server_inv)
    app_info = await bot.application_info()
    owner    = app_info.owner
    files    = [i for i in os.listdir(eyebleach_path) if os.path.splitext(i)[1] in ['.mp4','.jpg','.jpeg','.png']]
    inline   = False
    pics     = vids = 0
    for i in files:
        if os.path.splitext(i)[1] == '.mp4':    vids+=1
        else:                                   pics+=1

    # If the style is embed, makes an embed
    if style == 'Embed':
        content = ''
        embed   = Embed(colour=Colour(0xB000B5))
        embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
        embed.add_field(name='Name',       value=f'{bot.user}',                 inline=inline )
        embed.add_field(name='Ping',       value=f'{int(bot.latency*1000)}ms',  inline=inline )
        embed.add_field(name='Pictures',   value=f'{pics}',                     inline=True   )
        embed.add_field(name='Videos',     value=f'{vids}',                     inline=True   )
        embed.add_field(name='Facts',      value=f'{len(facts)}',               inline=True   )
        embed.add_field(name='Servers',    value=f'{len(bot.guilds)}',          inline=inline )
        embed.add_field(name='Developer',  value=f'<@{owner.id}>',              inline=inline )
    
    # Else, makes a neofetch style text
    else:
        embed    = None
        content  = nfetch.format(
            gre  = '\u001B[2;32m',
            blu  = '\u001B[2;34m',
            cyn  = '\u001B[2;36m',
            res  = '\u001B[0m',
            name = f'{bot.user}',
            id_  = f'{bot.user.id}',
            ping = f'{int(bot.latency*1000)}ms',
            pics = f'{pics}',
            vids = f'{vids}',
            fact = len(facts),
            serv = f'{len(bot.guilds)}',
            dev  = f'{owner}'
        )
        content  = f'```ansi\n{content}\n```'

    await msg.edit_original_response(content=content, embed=embed, view=view)



async def cat(ctx:ApplicationContext, type_:str, eyebleach_path:str, ascii_cats:list[str]):
    msg   = await ctx.respond(f'Enhancing...\n```\n{r.choice(ascii_cats)}```')

    exts  = ['png', 'jpg', 'jpeg', 'mp4'] if not type_ else (['png', 'jpg', 'jpeg'] if type_=='Picture' else ['mp4'])
    files = get_file_path(eyebleach_path, allowed_exts=exts, max_size=7.9*10**6)
    fname = files[0]['fname']
    fp    = files[0]['fp']
    file  = File(fp=fp, filename=fname)

    await msg.edit_original_response(content=None, file=file)



async def invite(ctx:ApplicationContext, bot_inv:str):
    await ctx.respond('Click the button below to add me to your server :)', view=InvView(bot_inv))



async def fact(ctx:ApplicationContext, facts:list[str]):
    await ctx.respond(r.choice(facts))








'''

'''

