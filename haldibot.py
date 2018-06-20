import io
import json
import datetime
import discord
import asyncio
from builtins import input
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
from discord.ext.commands import Bot
from discord.ext import commands
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
import platform

print("Loading NLU engine...")
# Load up Snips engine
load_resources(u"en")
engine = SnipsNLUEngine(config=CONFIG_EN)
with io.open('dataset.json') as f:
    dataset = json.load(f)
engine.fit(dataset)

client = Bot(description="haldibot.", command_prefix="-", pm_help = False)

@client.event
async def on_ready():
	return await client.change_presence(game=discord.Game(name='L E A R N I N G'))

@client.command()
async def echo(*args):

	response = " ".join(args)
	await client.say(response)

@client.command()
async def add(left: int, right: int):
	await client.say(left + right)

@client.command()
async def remind(*args):

	request = "remind " + " ".join(args)
	result = engine.parse(request)
	for s in result['slots']:
		if s['slotName'] == 'intent':
			intent = s['value']['value']
		if s['slotName'] == 'time':
			dt_string = s['value']['value']
	utc_offset = dt_string.rsplit(':', 1)
	dt_string = ''.join(utc_offset)
	format_string = "%Y-%m-%d %H:%M:%S %z"
	dt = datetime.datetime.strptime(dt_string, format_string)
	output_string_format = "%I:%M %p on %a, %b %d"
	output_time = datetime.datetime.strftime(dt, output_string_format)

	output_string = "I will remind me you to `{}` at `{}` (but not really, I haven't yet learned how)".format(intent, output_time)
	return await client.say(output_string)

@client.command(pass_context=True)
async def hello(ctx):
	message = "Hello, {}!  Have a nice day.".format(str(ctx.message.author).split('#')[0])
	return await client.say(message)

with open('discord.txt') as infile:
	token = infile.read()
client.run(token)