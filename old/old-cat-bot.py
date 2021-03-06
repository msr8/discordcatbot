from secret_stuff import TOKEN, PICS_PATH, PEOPLE, LAST_POST_CHANNEL_ID
from discord.ext import commands, tasks
import random as r
import time as t
import discord
import json
import os

START = int( t.time() )
INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=893261717155500082&permissions=274878023680&scope=bot'   #Send msges, Send msges in threads, Embed Links, Attach Files, Raed msg history
DELAY = 5*60				# 1 hour
PREFIX = 'c:'
DATA = os.path.join( os.path.dirname(__file__) , 'DATA' )
P = PREFIX
HELP = f'''`{P}?` | `{P}h` | `{P}help` | `{P}list` : Gives you a list of available commands
`{P}info` | `{P}about` : Tells stuff about the bot
`{P}ping` : Pings the bot and tells you its latency
`{P}cute` | `{P}cat` | `{P}ket` : Sends you a pic/vid of an angel
`{P}channel <channel>` : Sets the channel where the media is sent

The bot automatically sends a pic/vid every hour in the channel set up by `{P}channel <channel>`. In case you haven't set it up, please do it right now. To view which channel has been set up, just do `{P}channel`
Do `{P}help [command]` to view arguments, aliases, and description about that command
'''





def strm(month_int):
	month_lib = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12: 'December'}
	return month_lib[ month_int ]

def load_json(json_file):
	with open(json_file,'r') as f:
		ret = json.load(f)
	return ret

def save_json(dic,json_file):
	with open(json_file,'w') as f:
		json.dump(dic, f, indent=2, skipkeys=True, sort_keys=True)

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

async def get_last_posted():
	async for message in lp_channel.history(limit=1):
		return int(message.content)







# Does the help command shit
class CustomHelpCommand(commands.DefaultHelpCommand):
	def __init__ (self):
		super().__init__()

	# When typed "c:help"
	async def send_bot_help(self,mapping):
		ctx = self.get_destination()
		await ctx.send( f'Commands for <@{client.user.id}>:\n\n{HELP}' )

# Does the intent shit
intents = discord.Intents.default()
intents.members = True

client = commands.Bot( command_prefix=PREFIX, help_command=CustomHelpCommand(), intents=intents )





# Once ready
@client.event
async def on_ready():
	global my_owner, lp_channel
	# Changing bot's status
	activity = discord.Game('with my cat')
	await client.change_presence( activity=activity  )
	# Gets the last posted channel, aka the channel where bot's last post time is stored
	lp_channel = client.get_channel( LAST_POST_CHANNEL_ID )
	# Assigns the member object of my owner
	my_owner = (await client.application_info()).owner
	# Starts the loop to send cats
	main_loop.start()
	print(f'[USING {client.user}]')



# When joins a server
@client.event
async def on_guild_join(guild):
	# Tells my owner that I joined
	dm_channel = await my_owner.create_dm()
	await dm_channel.send( f'Ayo <@{guild.owner_id}> just added me to their server **{guild}**. Pog!' )
	# Tells the owner of the guild what to do
	owner = await client.fetch_user( guild.owner_id )
	dm_channel = await owner.create_dm()
	# Makes the embed
	embed = discord.Embed( title='About me' , description=f'Hello! I am <@{client.user.id}>! Here are some things you should know about me. If you are setting me up for the first time, please click at my documentation. Thank you for adding me to **{guild.name}** :)\n\n[GitHub](https://github.com/msr8/discordcatbot)' , colour=0xb00b69 )
	embed.set_author(name=client.user, icon_url=client.user.avatar_url)
	# Sends the embed
	await dm_channel.send(embed=embed)







# Help
@client.command( aliases=['?','h'], description='Gives you a list of all the available commands' )
async def list(ctx):
	await ctx.send( f'Commands for <@{client.user.id}>:\n\n{HELP}' )



# Info/About
@client.command( aliases=['info'], description='Tells stuff bout the bot' )
async def about(ctx):
	created = client.user.created_at
	# Creates the embed object
	embed = discord.Embed( title = client.user , description = f'Information about <@{client.user.id}>' , colour = discord.Colour.blue() )
	embed.set_footer(text = 'Have a nice day!')
	embed.set_author(name=client.user, icon_url=client.user.avatar_url)
	# Sets all the fields and gets all the info
	embed.add_field(name='Name',			value= client.user,												inline=True)
	embed.add_field(name='ID',				value= client.user.id,											inline=True)
	embed.add_field(name='Prefix',			value= f'`{PREFIX}`',											inline=True)
	embed.add_field(name='Created At',		value= f'{created.day} {strm(created.month)} {created.year}',	inline=True)
	embed.add_field(name='Uptime',			value= f'<t:{START}:R>',										inline=True)
	embed.add_field(name='Latency/Ping',	value= f'{int(client.latency*1000)} ms',						inline=True)
	embed.add_field(name='Total Servers',	value= len(client.guilds),										inline=True)
	embed.add_field(name='Owner', 			value= my_owner,												inline=True)
	embed.add_field(name='Github',			value= '[Github](https://github.com/msr8/discordcatbot)',		inline=True)
	embed.add_field(name='Invite',			value= f'[Invite]({INVITE_LINK})',								inline=True)
	await ctx.send(embed=embed)
# Documentation, support server, invite



# Ping
@client.command( description='Pings the bot and tells it\'s latency' )
async def ping(ctx):
	latency = int(client.latency*1000)
	await ctx.send(f'Latency: **{latency} ms**')




# Cute
@client.command( aliases=['cat','ket'], description='Sends you a pic of a cute animal, mostly cats' )
async def cute(ctx):
	cute_file_path = get_cute_pic_path()
	# Makes the discord file object
	to_send_cute_file = discord.File( cute_file_path, filename= os.path.basename(cute_file_path) )
	await ctx.send( file=to_send_cute_file )



# Channel
@client.command( description='Sets the channel where the media is sent' )
async def channel(ctx, channel : discord.TextChannel = None):
	guild = ctx.guild
	channels_data = load_json(channels_json)
	channel_old = channels_data.get(str(guild.id))
	# If no argument given, shows the channel set
	if channel == None:
		# If no channel is set
		if channel_old == None:
			await ctx.send(f'No media channel has been set for **{guild.name}**')
			return
		# If channel is set, tell which channel
		else:
			await ctx.send(f'<#{channel_old}> is the media channel for **{guild.name}**')
			return
	# If given argument, saves that channel in channel.json
	else:
		# Checks if they are owner. If they arent, tell them that and stops this function
		if not ctx.author.id == guild.owner_id:
			await ctx.send( f'I am sorry <@{ctx.author.id}> but only the server owner ({guild.owner}) can change the media channel ??\\_(???)_/??' )
			return
		channels_data[str(guild.id)] = str(channel.id)
		save_json(channels_data, channels_json)
		await ctx.send(f'<#{channel.id}> has been set as the media channel for **{guild.name}**')















@tasks.loop( minutes=1 )
async def main_loop():
	# Checks if its been an hr since last posted
	if not int(t.time()) - DELAY > await get_last_posted():
		return
	# Gets data inside channels.json
	channels_data = load_json(channels_json)
	# Loops thro them and gets the channel
	for guild_id in channels_data.keys():
		try:
			channel = await client.fetch_channel( channels_data[guild_id] )
			# Sends stuff to the channel
			# Gets the path of the file to send
			cute_file_path = get_cute_pic_path()
			# Makes the discord file object
			to_send_cute_file = discord.File( cute_file_path, filename= os.path.basename(cute_file_path) )
			await channel.send( file=to_send_cute_file )
				
		# In case of error, prints it and tries to message owner about it
		except Exception as e:
			channel_id = channels_data[guild_id]
			print(f'Channel Error: {guild_id} | {channel_id} | {e}')
			# Tries to msg owner about it
			try:
				# Gets guild object of which guild the channel was in
				guild = await client.fetch_guild(guild_id)
				# Gets owner of that guild
				owner = await client.fetch_user(guild.owner_id)
				# Gets DM channel with the owner
				dm_channel = await owner.create_dm()
				# Checks if their last message was 'STOP'
				async for message in dm_channel.history(limit=1):
					can_msg = False if message.content == 'STOP' else True
				# If we can message, we message
				if can_msg:
					await dm_channel.send(f'Please set up the bot in another channel of **{guild.name}** since I can\'t message in <#{channel_id}> anymore. If you would like to stop recieving messages about setting up the bot, please message "STOP". If you want to resume the messages, just delete the "STOP" message')
			except Exception as e:
				print(f'DM Error: {guild_id} | {e}')
	# Messages in last posted channel
	await lp_channel.send( int(t.time()) )











# Initialisation

# DATA folder
if not os.path.exists(DATA):
	os.makedirs(DATA)
# channels.json
channels_json = os.path.join(DATA,'channels.json')
if not os.path.isfile(channels_json):
	save_json({}, channels_json)



client.run(TOKEN)



