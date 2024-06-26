from discord              import Colour, Embed
from discord.ui           import View, Button
from discord.commands     import ApplicationContext
from discord.ext.commands import Bot

from datetime import datetime as dt
import random as r






class MyView(View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, bot_inv:str, server_inv:str):
        super().__init__()

        self.add_item(Button(label='Bot Invite',      url=bot_inv))
        self.add_item(Button(label='Website',         url='https://msr8.dev/cats'))
        self.add_item(Button(label='Source Code',     url='https://github.com/msr8/discordcatbot'))
        self.add_item(Button(label='Support Server',  url=server_inv))


class InvView(View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, bot_inv:str):
        super().__init__()
        self.add_item(Button(label='Invite',          url=bot_inv))






# async def ping(ctx:ApplicationContext, bot:Bot):
#     latency = int(bot.latency*1000)
#     await ctx.respond(f'My latency is {latency}ms')







async def about(ctx:ApplicationContext, bot:Bot, style:str, nfetch:str, facts:list, files_info_json:dict, bot_inv:str, server_inv:str):
    msg = await ctx.respond('```\nCalculating...```')

    view     = MyView(bot_inv, server_inv)
    app_info = await bot.application_info()
    owner    = app_info.owner
    inline   = False
    pics     = files_info_json['total_images']
    # If the style is embed, makes an embed
    if style == 'Embed':
        content      = ''
        embed       = Embed()
        embed.color = 0xB000B5
        embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
        embed.set_footer(text='To view all my commands, please do /help')
        embed.add_field(name='Name',       value=f'{bot.user}',                 inline=inline )
        embed.add_field(name='Ping',       value=f'{int(bot.latency*1000)}ms',  inline=inline )
        embed.add_field(name='Images',     value=f'{pics}',                     inline=True   )
        embed.add_field(name='Facts',      value=f'{len(facts)}',               inline=True   )
        embed.add_field(name='Servers',    value=f'{len(bot.guilds)}',          inline=inline )
        embed.add_field(name='Developer',  value=f'{owner}',                    inline=inline )
    
    # Else, makes a neofetch style text, ██
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
            fact = len(facts),
            serv = f'{len(bot.guilds)}',
            dev  = f'{owner}'
        )
        content  = f'```ansi\n{content}\n```'

    await msg.edit_original_response(content=content, embed=embed, view=view)



async def cat(ctx:ApplicationContext, files_json:dict, ascii_cats:list[str]):
    msg = await ctx.respond(f'Enhancing...\n```\n{r.choice(ascii_cats)}```')

    # Gets the cat
    file_ids = list(files_json['data'].values())
    while True:
        file = r.choice(file_ids)
        if file['type'] == 'image': break

    # Makes the embed
    embed      = Embed()
    color      = 0xB000B5
    ts         = dt.fromtimestamp(file["created_utc"]).strftime('%-d/%-m/%y (%H:%M)')
    author     = f'r/{file["subreddit"]}'
    author_url = f'https://reddit.com/r/{file["subreddit"]}'
    desc       = f'**[{file["title"]}]({file["post_url"]})**'
    img_url    = file['media_url']
    footer     = f'u/{file["op"]}   •   {ts}'

    embed.description = desc
    embed.color = color
    embed.set_author(name = author, url = author_url)
    embed.set_image (url  = img_url)
    embed.set_footer(text = footer)

    await msg.edit_original_response(content=None, embed=embed)



async def invite(ctx:ApplicationContext, bot_inv:str):
    await ctx.respond('Click the button below to add me to your server :)', view=InvView(bot_inv))



async def fact(ctx:ApplicationContext, facts:list[str]):
    await ctx.respond(r.choice(facts))



async def help(ctx:ApplicationContext, bot:Bot, help_dict:list):
    embed       = Embed()
    embed.title = 'My commands!'
    embed.color = 0xB000B5
    embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
    # Adds all the attributes
    for k in help_dict:
        embed.add_field(name=f'`/{k}`', value=help_dict[k], inline=False)

    await ctx.respond(embed=embed)






