import io
import json
import datetime
import discord
import asyncio
import pytz
from random import randint
from builtins import input
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
from discord.ext.commands import Bot
from discord.ext import commands
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
from dateutil import parser
from datetime import timezone
import platform
from reminder import set_reminder
from weather import get_weather

print("Loading NLU engine...")
# Load up Snips engine
load_resources(u"en")
engine = SnipsNLUEngine(config=CONFIG_EN)
#with io.open('data/dataset.json') as f:
#    dataset = json.load(f)
#engine.fit(dataset)
engine = SnipsNLUEngine.from_path("engine")

client = Bot(description="haldibot.", command_prefix="-", pm_help = False)

print("haldibot lives!")

@client.event
async def on_ready():
	return await client.change_presence(game=discord.Game(name='with time zones'))

@client.command()
async def fuckyou(*args):
	response = "no fuck you"
	await client.say(response)

@client.command()
async def echo(*args):
	response = " ".join(args)
	await client.say(response)

@client.command()
async def add(left: int, right: int):
	await client.say(left + right)

@client.command()
async def subtract(left: int, right: int):
	await client.say(left - right)

@client.command()
async def weather(*args):
	location = " ".join(args)
	weather_data = get_weather(location)
	return await client.say(weather_data)

@client.command(pass_context=True)
async def remind(ctx, *args):

	request = "remind " + " ".join(args)
	result = engine.parse(request)
	intent = None
	dt_string = None
	if not result['slots']:
		return await client.say("I can't **** understand **** your accent ****")
	for s in result['slots']:
		if s['slotName'] == 'intent':
			intent = s['value']['value']
		if s['slotName'] == 'time':
			dt_string = s['value']['value']
	if not intent:
		return await client.say("It isn't clear to me what to remind you about.")
	if not dt_string:
		return await client.say("I know what you want to be reminded of, but not what time to remind you.")
	dt = parser.parse(dt_string)
	new_dt = dt.astimezone(tz=None)
	user_id = ctx.message.author.id
	channel_id = ctx.message.channel.id
	set_reminder(intent, new_dt, user_id, channel_id)
	
	output_string_format = "%I:%M %p on %a, %b %d"
	output_time = datetime.datetime.strftime(dt, output_string_format)

	output_string = "<@{}>, I will remind me you to `{}` at `{} UTC`".format(user_id, intent, output_time)
	return await client.say(output_string)

@client.command(pass_context=True)
async def hello(ctx):
	message = "Hello, <@{}>!  Have a nice day.".format(str(ctx.message.author.id))
	return await client.say(message)

@client.command()
async def eightball():
	vals = [
		'It is certain.',
		'It is decidedly so',
		'Without a doubt.',
		'Yes - definitely',
		'You may rely on it.',
		'As I see it, yes.',
		'Most likely',
		'Outlook good.',
		'Yes',
		'Signs point to yes.',
		'Reply hazy, try again.',
		'Ask again later.',
		'Better not tell you now.',
		'Cannot predict now.',
		'Concentrate and ask again.',
		"Don't count on it.",
		'My reply is no.',
		'My sources say no.',
		'Outlook not so good.',
		'Very doubtful.'
	]
	val = vals[randint(0,len(vals) - 1)]
	return await client.say(val)

with open('discord.txt') as infile:
	token = infile.read()
client.run(token)
