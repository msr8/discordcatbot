from secret_stuff import TOKEN, PICS_PATH, PEOPLE
from discord.ext import commands, tasks
import random as r
import time as t
import discord
import os


PREFIX = 'c:'
INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=893261717155500082&permissions=274878023680&scope=bot'
DATA = os.path.join( os.path.dirname(__file__) , 'DATA' )
CHANNELS = os.path.join( DATA, 'channels' )
P = PREFIX

HELP = f'''`{P}?` | `{P}h` | `{P}help` | `{P}list` : Gives you a list of available commands
`{P}ping` : Pings the bot and tells you its latency
`{P}info` | `{P}about` : Tells stuff about the bot
`{P}channel help` | `{P}channels help` : Shows the commands used to set up this bot
`{P}cute` | `{P}cat` | `{P}ket` : Sends you a pic/vid of a cute animal (mostly cats)'''

CHANNEL_HELP = help_text = f'''`{P}channel help` : Shows this message
`{P}channel <list | ls>` : Shows all the allowed channels in this server
`{P}channel allow <channel>` or `{P}channel add <channel>` : Allows a channel
`{P}channel disallow <channel>` or `{P}channel remove <channel>` : Disallows a channel'''






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
		to_send = f'I am not allowed to send messages in this server ({guild.name}). If you want me to send messages in this server, contact the mods of this server. If you are a mod and are trying to set me up in your server, do `c:channel add <channel>` with the channel you want to allow me to send messages in. In case of any further queries, check out my [GitHub](https://github.com/msr8/discordcatbot)'
	# If there are allowed channels
	else:
		to_send = f'I am not allowed to send messages in <#{channel.id}> of the server **{guild.name}**, I can only send messages in the following channels:\n\n'
		for channel in channels:
			to_send += f'<#{channel}>\n'
	# Sends the DM
	await dm_channel.send(embed=discord.Embed( description=to_send , colour=discord.Colour.red() ))

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
	




















# Once ready
@bot.event
async def on_ready():
	print(f'[USING {bot.user}]')









# Help
@bot.command( aliases=['?','list'], description='Gives you a list of all the available commands' )
async def h(ctx):
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		await send_dm(ctx)
		return
	await ctx.reply( f'Commands for <@{bot.user.id}>:\n\n{HELP}' )




# Ping
@bot.command( description='Pings the bot and tells it\'s latency' )
async def ping(ctx):
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		await send_dm(ctx)
		return
	latency = int(bot.latency*1000)
	await ctx.reply(f'**Latency:** {latency}ms')




# Info
@bot.command( aliases=['about'] )
async def info(ctx):
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		await send_dm(ctx)
		return
	embed = discord.Embed( title=bot.user , description=f'Information about <@{bot.user.id}>' , colour=discord.Colour.blue() )
	embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
	# Adds Name, ID, Prefix, Ping, Total Servers, Owner, Github, Invite
	embed.add_field(name='Name',value=bot.user)
	embed.add_field(name='ID',value=bot.user.id)
	embed.add_field(name='Prefix',value=PREFIX)
	embed.add_field(name='Ping',value=f'{int(bot.latency*1000)}ms')
	embed.add_field(name='Total Servers',value=len(bot.guilds))
	embed.add_field(name='Owner',value=f'<@{PEOPLE["me"]}>')
	embed.add_field(name='GitHub',value='[GitHub](https://github.com/msr8/discordcatbot)')
	embed.add_field(name='Invite',value=f'[Invite]({INVITE_LINK})')
	# Sends the Embed
	await ctx.reply(embed=embed)




# Cat | Cute
@bot.command( aliases=['cute','ket'] )
async def cat(ctx):
	# Checks if I am allowed to send msges in this channel
	if not str(ctx.channel.id) in get_channels(ctx.guild):
		await send_dm(ctx)
		return
	await ctx.reply(file=discord.File( get_cute_pic_path() ))




# Channel
@bot.command( aliases=['channels'] )
async def channel(ctx, setting=None, channel:discord.TextChannel=None):
	# Checks if author has manage channels permission
	if not ctx.author.guild_permissions.manage_channels:
		# Sends a DM explaining they dont have perms
		dm_channel = await ctx.author.create_dm()
		await dm_channel.send(embed=discord.Embed( description=f'I am sorry but only people who have the `Manage Channels` permissions can do `{P}channel`. If you think there has been an error, please contact my developer <@{PEOPLE["me"]}> or open up an issue on my [github](https://github.com/msr8/discordcatbot)' , colour=discord.Colour.red() ))
		return

	# Checks if its a valid setting
	if setting == None or not setting.lower() in ['help','h','?','list','ls','allow','add','disallow','remove']:
		await ctx.reply(embed = discord.Embed( description=f'{setting} is not a valid setting, please do `{P}channel help` to view all the valid settings' , colour=discord.Colour.red() ))
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
		# Adds the channel
		channels.remove(str(channel.id))
		# Dumps the data
		dump_channels(channels,ctx.guild)
		# Tells the user its done
		await ctx.reply(embed=discord.Embed( description=f'<#{channel.id}> has been succesfully removed from the list of allowed channels' , colour=discord.Colour.blue() ))
































for path in [DATA,CHANNELS]:
	if not os.path.exists(path):
		os.makedirs(path)





bot.run(TOKEN)





