from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, create_select, create_select_option
from discord_slash import SlashCommand, SlashContext
from secret_stuff import TOKEN, PICS_PATH, PEOPLE
from colorama import init, Fore, Back, Style
from discord_slash.model import ButtonStyle
from discord.ext import commands
import requests as rq
import random as r
import time as t
import discord
import os
init()



PREFIX = 'c:'
DATA = os.path.join( os.path.dirname(__file__) , 'DATA' )
CHANNELS = os.path.join( DATA, 'channels' )
GITHUB_LINK = 'https://github.com/msr8/discordcatbot'
DOCUMENTATION_LINK = 'https://msr8.github.io/discordcatbot/'
SERVER_INVITE = 'https://discord.gg/aGUvpSxMz5'
BOT_INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=893261717155500082&permissions=274878024704&scope=applications.commands%20bot' # With perms 274878024704
RES = Style.RESET_ALL
GR = Fore.GREEN
YE = Fore.YELLOW
uptime_count = 0
P = PREFIX

HELP = f'''`{P}?` | `{P}h` | `{P}help` | `{P}list` : Gives you a list of available commands
`{P}ping` : Pings the bot and tells you its latency
`{P}info` | `{P}about` : Tells stuff about the bot
`{P}channel help` | `{P}channels help` : Shows the commands used to set up this bot
`{P}cute` | `{P}cat` | `{P}ket` : Sends you a pic/vid of a cute animal (mostly cats)
\n__SLASH COMMANDS__\n
`/help` : Gives you a list of available commands
`/about` : Tells stuff about the bot
`/cat` : Sends you a pic/vid of a cute animal (mostly cats)
`/settings` : Basically `{P}channel` but GUI
'''

CHANNEL_HELP = help_text = f'''`{P}channel help` : Shows this message
`{P}channel <list | ls>` : Shows all the allowed channels in this server
`{P}channel allow <channel>` or `{P}channel add <channel>` : Allows a channel
`{P}channel disallow <channel>` or `{P}channel remove <channel>` : Disallows a channel
`{P}channel flush` : Removes all the deleted channels from our database'''

LINK_ACTROW = create_actionrow(
	create_button(style=ButtonStyle.URL, label='Documentation',		url=DOCUMENTATION_LINK	),
	create_button(style=ButtonStyle.URL, label='GitHub',			url=GITHUB_LINK			),
	create_button(style=ButtonStyle.URL, label='Support Server',	url=SERVER_INVITE		),
	create_button(style=ButtonStyle.URL, label='Bot Invite',		url=BOT_INVITE_LINK		),
	)






# Does the help command shit
class CustomHelpCommand(commands.DefaultHelpCommand):
	def __init__ (self):
		super().__init__()

	# When typed "c:help"
	async def send_bot_help(self,mapping):
		channel = self.get_destination()
		# Checks if I am allowed to send msges in this channel
		if not str(channel.id) in get_channels(channel.guild):
			return
		await channel.send( f'Commands for <@{bot.user.id}>:\n\n{HELP}' )


bot = commands.Bot( command_prefix=PREFIX, help_command=CustomHelpCommand() )
slash = SlashCommand(bot, sync_commands=True)








cls = lambda: os.system('cls' if SYSTEM=='Windows' else 'clear')

def get_channels(guild):
	# Gets path of the file
	file_path = os.path.join(CHANNELS,f'{guild.id}.txt')
	# Checks if its exists
	if not os.path.exists(file_path):
		return []
	# Gets the data
	with open(file_path) as f:
		ret = [i.strip() for i in f.readlines()]
	return ret

def dump_channels(channels, guild):
	# Gets path of the file
	file_path = os.path.join(CHANNELS,f'{guild.id}.txt')
	to_dump = '\n'.join(channels)
	# Writes the data
	with open(file_path,'w') as f:
		f.write(to_dump)

async def send_dm(ctx):
	# Gets all the attributes
	dm_channel = await ctx.author.create_dm()
	channel = ctx.channel
	guild = ctx.guild
	channels = get_channels(guild)
	# If there are no allowed channels
	if not len(channels):
		to_send = f'I am not allowed to send messages in this server ({guild.name}). If you want me to send messages in this server, contact the mods of this server. If you are a mod and are trying to set me up in your server, do `c:channel add <channel>` with the channel you want to allow me to send messages in. In case of any further queries, please check out the links given below'
		components = [LINK_ACTROW]
	# If there are allowed channels
	else:
		to_send = f'I am not allowed to send messages in <#{channel.id}> of the server **{guild.name}**, I can only send messages in the following channels:\n\n'
		for channel in channels:
			to_send += f'<#{channel}>\n'
		components = []
	# Sends the DM
	embed=discord.Embed( description=to_send , colour=discord.Colour.red() )
	await dm_channel.send(embed=embed, components=components)

def get_cute_pic_path():
	# Gets all the files and folders of the main directory where the pictures are stored
	all_stuff = os.listdir(PICS_PATH)
	# Loops thro them and checks if they are valid enough to be sent
	eyebleach_valid = False
	while not eyebleach_valid:
		fil = r.choice(all_stuff)
		fil_path = os.path.join( PICS_PATH,fil )
		# Checks if they are a file, are not chache, and are lower than 7.9mb (just to be safe)
		if os.path.isfile(fil_path) and (not fil.startswith('.')) and os.stat(fil_path).st_size < 7.9*10**6:
			valid_file = fil_path
			eyebleach_valid = True
	# Returns the valid file path
	return valid_file

async def make_chc_comp(ctx):
	channels = ctx.guild.text_channels
	allowed_channels = [await bot.fetch_channel(i) for i in get_channels(ctx.guild)]
	for i in allowed_channels:
		try:
			channels.remove(i)
		except:
			continue
	options=[]
	for channel in channels:
		options.append( create_select_option(channel.name, value=str(channel.id)) )
	actrow = create_actionrow(create_select( options=options , max_values=len(channels) ))
	return actrow

async def make_chc_comp_2(ctx):
	old_channels = get_channels(ctx.guild)
	channels = []
	for i in old_channels:
		try:
			channels.append(await bot.fetch_channel(i))
		except:
			continue
	options = []
	for channel in channels:
		options.append( create_select_option(channel.name, value=str(channel.id)) )
	actrow = create_actionrow(create_select( options=options , max_values=len(channels) ))
	return actrow




async def send_cat(ctx):
	# Checks if its not a DM channel
	if not isinstance(ctx.channel, discord.DMChannel):
		# Checks if I am not allowed to send msges in this channel
		if not str(ctx.channel.id) in get_channels(ctx.guild):
			# Checks if its a slash command:
			if isinstance(ctx, SlashContext):
				await ctx.reply(file=discord.File( get_cute_pic_path() ), hidden=True)
				return
			await send_dm(ctx)
			return
	await ctx.reply(file=discord.File( get_cute_pic_path() ))


async def send_about(ctx, slash_com=False):
	# if its a slash command, gives in hidden
	if not slash_com:
		# Checks if I am allowed to send msges in this channel
		if not str(ctx.channel.id) in get_channels(ctx.guild):
			await send_dm(ctx)
			return
	embed = discord.Embed( title=f'Information about {bot.user}' , description=f'Hi! I am <@{bot.user.id}> made by <@{PEOPLE["me"]}>. What I basically do is send cat pictures/video whenever you ask me to. To use me, you first have to set me up using `{P}channel` or `/setting`. Then to get cat stuff, you can simply type `{P}cat` or `/cat` in the allowed channels. To see all my commands, do `{P}help` or `/help` if you want to learn more about me or having trouble setting it up, check out the links below :)\n\nNOTE: I do not claim any ownership of the cats. All of the media used was obtained from public sources (mostly reddit)' , colour=discord.Colour.blue() )
	embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
	# Adds Name, ID, Prefix, Ping, Total Servers, Owner, Github, Invite
	embed.add_field(name='Name',			value=bot.user									)
	embed.add_field(name='ID',				value=bot.user.id								)
	embed.add_field(name='Prefix',			value=f'`{PREFIX}`'								)
	embed.add_field(name='Ping',			value=f'{int(bot.latency*1000)}ms'				)
	embed.add_field(name='Total Servers',	value=len(bot.guilds)							)
	embed.add_field(name='Owner',			value=f'<@{PEOPLE["me"]}>'						)
	embed.add_field(name='Documentation',	value=f'[Documentation]({DOCUMENTATION_LINK})'	)
	embed.add_field(name='GitHub',			value=f'[GitHub]({GITHUB_LINK})'				)
	embed.add_field(name='Support Server',	value=f'[Support Server]({SERVER_INVITE})'		)
	embed.add_field(name='Bot Invite',		value=f'[Invite]({BOT_INVITE_LINK})'			)
	# Sends the Embed
	if not slash_com:
		await ctx.reply(embed=embed)
		return
	await ctx.reply(embed=embed, hidden=True)


async def send_fact(ctx):
	fact = rq.get('https://catfact.ninja/fact').json()['fact']
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		# Checks if its a slash command
		if not isinstance(ctx, SlashContext):
			await send_dm(ctx)
			return
		await ctx.reply(fact, hidden=True)
		return
	await ctx.reply(fact)
	






















# Once ready
@bot.event
async def on_ready():
	global uptime_count
	uptime_count += 1
	if uptime_count > 1:
		# LOG
		print(f'\n{YE}[{bot.user} is up at {t.asctime()}]{RES}')
		return
	# Changing bot's status
	status = discord.Status.idle
	activity = discord.Game('with my cat')
	await bot.change_presence(status=status, activity=activity)
	print(f'{GR}[USING {bot.user}]{RES}')
	print( '\n'.join( [f'{i.id} : {i.name}' for i in bot.guilds] ) )

# When joined a guild
@bot.event
async def on_guild_join(guild):
	# Gets the DM channel of the owner
	owner = await bot.fetch_user( guild.owner_id )
	dm_channel = await owner.create_dm()
	# Sends them an introduction
	embed = discord.Embed( title='About me' , description=f'Hello! I am <@{bot.user.id}>! To use me, you can tell me which channels I am allowed send messages in by doing `c:channel add <channel>` or using `/settings` (I would reccomend using normal commands instead of slash commands because in the current state, slash commands are a lil bit glitchy). Once the channel is allowed, you can do `c:cat` or `/cat` to get a picture/video of a cat (mostly). To view all of my commands, you can do `c:help` or `/help`. For futher help, check out the links given below. Thank you for inviting me to **{guild}** :)' , colour=0xb00b69 )
	await dm_channel.send(embed=embed, components=[LINK_ACTROW])
	# Tells my owner I joined the server
	my_owner = await bot.fetch_user( PEOPLE['me'] )
	dm_channel = await my_owner.create_dm()
	await dm_channel.send(f'<@{owner.id}> just added me to **{guild.name}**!')












# Help
@bot.command( aliases=['?','list'], description='Gives you a list of all the available commands' )
async def h(ctx):
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		await send_dm(ctx)
		return
	await ctx.reply( f'Commands for <@{bot.user.id}>:\n\n{HELP}', components=[LINK_ACTROW] )
@slash.slash( name='help' , description='Gives you a list of all the available commands' )
async def help_slash(ctx: SlashContext):
	await ctx.reply(f'Commands for <@{bot.user.id}>:\n\n{HELP}', components=[LINK_ACTROW], hidden=True)




# Ping
@bot.command( description='Pings the bot and tells it\'s latency' )
async def ping(ctx):
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		await send_dm(ctx)
		return
	latency = int(bot.latency*1000)
	await ctx.reply(f'**Latency:** {latency}ms')




# About | Info
@bot.command( aliases=['about'] , description='Tells you stuff about the bot' )
async def info(ctx):
	await send_about(ctx)
@slash.slash( name='about' , description='Tells you stuff about the bot' )
async def info1(ctx: SlashContext):
	await send_about(ctx, slash_com=True)




# Cat | Cute | Ket
@bot.command( aliases=['cute','ket'] , description='Sends you a picture/video of a cat (mostly)' )
async def cat(ctx):
	await send_cat(ctx)
@slash.slash( name='cat' , description='Sends you a picture/video of a cat (mostly)' )
async def cat1(ctx: SlashContext):
	await send_cat(ctx)




# Fact
@bot.command( description='Sends you a random fact about cats' )
async def fact(ctx):
	await send_fact(ctx)
@slash.slash( name='fact' , description='Sends you a random fact about cats' )
async def fact1(ctx: SlashContext):
	await send_fact(ctx)




# Channel
@bot.command( aliases=['channels'] , description=f'Helps you manage which channels the bot can send the message in. Do `{P}channels help` to learn more' )
async def channel(ctx, setting=None, channel:discord.TextChannel=None):
	# Checks if author has manage channels permission
	if not ctx.author.guild_permissions.manage_channels:
		# Sends a DM explaining they dont have perms
		dm_channel = await ctx.author.create_dm()
		embed=discord.Embed( description=f'I am sorry but only people who have the `Manage Channels` permissions can do `{P}channel`. If you think there has been an error, please check the links given below' , colour=discord.Colour.red() )
		await dm_channel.send(embed=embed, components=[LINK_ACTROW])
		return

	setting = setting.lower()

	# Help
	if setting in ['help','h','?']:
		await ctx.reply(embed=discord.Embed( description=f'**All the commands for `{P}channel` of <@{bot.user.id}>:**\n\n'+CHANNEL_HELP , colour=discord.Colour.blue() ))
		return

	# List | ls
	elif setting in ['list','ls']:
		# Gets the channels
		channels = get_channels(ctx.guild)
		channels = [str(i) for i in channels]
		# Checks if there are no channels
		if not len(channels):
			await ctx.reply('There are no allowed channels for this server')
		# Else lists the channels
		else:
			channel_text = f'**Allowed channels for {ctx.guild}:**\n\n'
			for channel in channels:
				channel_text += f'<#{channel}>\n'
			await ctx.reply(embed=discord.Embed( description=channel_text , colour=discord.Colour.blue() ))

	# Flush
	elif setting in ['flush']:
		channels = get_channels(ctx.guild)
		channels = [str(i) for i in channels]
		count = 0
		for i in channels:
			try:
				channel = await bot.fetch_channel(i)
			except:
				channels.remove(i)
				count += 1
		dump_channels(channels, ctx.guild)
		await ctx.reply(embed=discord.Embed( description='No deleted channels found' if count==0 else f'{count} deleted channel(s) removed'  , colour=discord.Colour.red() if count==0 else discord.Colour.blue()  ))

	# Allow
	elif setting in ['allow','add']:
		# Checks if channel given
		if not channel:
			await ctx.reply('Please provide a channel which you want to allow')
			return
		# Gets the channels
		channels = get_channels(ctx.guild)
		channels = [str(i) for i in channels]
		# Checks if its an already allowed channel
		if str(channel.id) in channels:
			ctx.reply(f'<#{channel.id}> is already an allowed channel')
			return
		# Adds the channel
		channels.append(str(channel.id))
		# Dumps the data
		dump_channels(channels,ctx.guild)
		# Tells the user its done
		await ctx.reply(embed=discord.Embed( description=f'<#{channel.id}> has been succesfully set as an allowed channel' , colour=discord.Colour.blue() ))
		
	# Disallow
	elif setting in ['disallow','remove']:
		# Checks if channel given
		if not channel:
			await ctx.reply('Please provide a channel which you want to allow')
			return
		# Gets the channels
		channels = get_channels(ctx.guild)
		channels = [str(i) for i in channels]
		# Checks if it isnt an allowed channel
		if not str(channel.id) in channels:
			ctx.reply(f'<#{channel.id}> is not an allowed channel')
			return
		# Removes the channel
		channels.remove(str(channel.id))
		# Dumps the data
		dump_channels(channels,ctx.guild)
		# Tells the user its done
		await ctx.reply(embed=discord.Embed( description=f'<#{channel.id}> has been succesfully removed from the list of allowed channels' , colour=discord.Colour.blue() ))

	# Not a valid option
	else:
		await ctx.reply(embed = discord.Embed( description=f'{setting} is not a valid setting, please do `{P}channel help` to view all the valid settings' , colour=discord.Colour.red() ))







async def settings_func(ctx):
	# Checks if author has manage channels permission
	if not ctx.author.guild_permissions.manage_channels:
		# Tells them that they need perms
		await ctx.reply(f'I am sorry but only people who have the `Manage Channels` permissions can do `/settings`. If you think there has been an error, please check out the links given below', components=[LINK_ACTROW], hidden=True)
		return

	chc_actrow = create_actionrow(
		create_button(style=ButtonStyle.blue, label='Help'),
		create_button(style=ButtonStyle.blue, label='List'),
		create_button(style=ButtonStyle.blue, label='Allow a channel'),
		create_button(style=ButtonStyle.blue, label='Disallow a channel'),
		create_button(style=ButtonStyle.blue, label='Flush'),
		)
	chc_actrow2 = create_actionrow(create_button(style=ButtonStyle.blue, label='Exit'))
	embed = discord.Embed( description='Please select what you want to do' , colour=discord.Colour.blue() )
	await ctx.reply(embed=embed, components=[chc_actrow,chc_actrow2])
	# Checks if the author is clicking the buttons
	while True:
		comp_ctx:ComponentContext = await wait_for_component(bot, components=[chc_actrow,chc_actrow2])
		if ctx.author.id == comp_ctx.author.id:
			break
	chc = comp_ctx.component['label']
	
	if chc == 'Help':
		embed = discord.Embed( description='**Help:** Shows this message\n**List:** Shows all the allowed channels in this server\n**Allow:** Allows a channel\n**Disallow:** Disallows a channel\n**Flush:** Removes all the deleted channels from our database' , colour=discord.Colour.blue() )
		await comp_ctx.edit_origin(embed=embed, components=None, hidden=True)
	
	elif chc == 'List':
		# Gets the channels
		channels = get_channels(ctx.guild)
		channels = [str(i) for i in channels]
		# Checks if there are no channels
		if not len(channels):
			channel_text = 'There are no allowed channels for this server'
		else:
			channel_text = f'**Allowed channels for {ctx.guild}:**\n\n'
			for channel in channels:
				channel_text += f'<#{channel}>\n'
		embed = discord.Embed( description=channel_text , colour=discord.Colour.blue() )
		await comp_ctx.edit_origin(embed=embed, components=[])

	elif chc == 'Allow a channel':
		allow_actrow = await make_chc_comp(ctx)
		await comp_ctx.edit_origin(components=[allow_actrow])
		# Checks if the author is clicking the buttons
		while True:
			comp_ctx:ComponentContext = await wait_for_component(bot, components=[allow_actrow])
			if ctx.author.id == comp_ctx.author.id:
				break
		allow_chc = comp_ctx.selected_options
		# Gets old channels
		channels = get_channels(ctx.guild)
		# Adds channels
		for channel in allow_chc:
			if channel not in channels:
				channels.append(channel)
		# Dumps the data
		dump_channels(channels, ctx.guild)
		# Tells the user its done
		embed = discord.Embed( description='Success!' , colour=discord.Colour.blue() )
		await comp_ctx.edit_origin(embed=embed, components=[])

	elif chc == 'Disallow a channel':
		disallow_actrow = await make_chc_comp_2(ctx)
		await comp_ctx.edit_origin(components=[disallow_actrow])
		# Checks if the author is clicking the buttons
		while True:
			comp_ctx:ComponentContext = await wait_for_component(bot, components=[disallow_actrow])
			if ctx.author.id == comp_ctx.author.id:
				break
		disallow_chc = comp_ctx.selected_options
		# Gets the old channels
		channels = get_channels(ctx.guild)
		# Removes channels
		for channel in disallow_chc:
			if channel in channels:
				channels.remove(channel)
		# Dumps the data
		dump_channels(channels, ctx.guild)
		# Tells the user its done
		embed = discord.Embed( description='Success!' , colour=discord.Colour.blue() )
		await comp_ctx.edit_origin(embed=embed, components=[])

	elif chc == 'Flush':
		channels = get_channels(ctx.guild)
		channels = [str(i) for i in channels]
		count = 0
		for i in channels:
			try:
				channel = await bot.fetch_channel(i)
			except:
				channels.remove(i)
				count += 1
		dump_channels(channels, ctx.guild)
		# Tells the user its done
		embed = discord.Embed( description='No deleted channels found' if count==0 else f'Success! {count} deleted channel(s) removed' , colour=discord.Colour.blue() )
		await comp_ctx.edit_origin(embed=embed, components=[])

	elif chc == 'Exit':
		await comp_ctx.origin_message.delete()




@slash.slash( name='settings' , description='Configure the bot' )
async def settings(ctx: SlashContext):
	await settings_func(ctx)
























for path in [DATA,CHANNELS]:
	if not os.path.exists(path):
		os.makedirs(path)




cls()

bot.run(TOKEN)





