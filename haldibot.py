import sys
import json
import boto3

from random import randint

import requests
import discord
from discord.ext import commands
from discord_commands import get_message

# OLD
# @client.event
# async def on_ready():
# 	return await client.change_presence(game=discord.Game(name='with time zones'))


# @client.command()
# async def weather(*args):
# 	location = " ".join(args)
# 	weather_data = get_weather(location)
# 	return await client.say(weather_data)

# @client.command(pass_context=True)
# async def remind(ctx, *args):

# 	request = "remind " + " ".join(args)
# 	result = engine.parse(request)
# 	intent = None
# 	dt_string = None
# 	if not result['slots']:
# 		return await client.say("I can't **** understand **** your accent ****")
# 	for s in result['slots']:
# 		if s['slotName'] == 'intent':
# 			intent = s['value']['value']
# 		if s['slotName'] == 'time':
# 			dt_string = s['value']['value']
# 	if not intent:
# 		return await client.say("It isn't clear to me what to remind you about.")
# 	if not dt_string:
# 		return await client.say("I know what you want to be reminded of, but not what time to remind you.")
# 	dt = parser.parse(dt_string)
# 	new_dt = dt.astimezone(tz=None)
# 	user_id = ctx.message.author.id
# 	channel_id = ctx.message.channel.id
# 	set_reminder(intent, new_dt, user_id, channel_id)
	
# 	output_string_format = "%I:%M %p on %a, %b %d"
# 	output_time = datetime.datetime.strftime(dt, output_string_format)

# 	output_string = "<@{}>, I will remind me you to `{}` at `{} UTC`".format(user_id, intent, output_time)
# 	return await client.say(output_string)

secrets_client = boto3.client('secretsmanager', region_name='us-west-2')

# Use dev token if we're testing on windows machine
token_secret_name = "discordBotTokenDev" if sys.platform == "win32" else "discordBotToken"
token_response = secrets_client.get_secret_value(SecretId=token_secret_name)
token_response_dict = json.loads(token_response['SecretString'])
discord_token = token_response_dict[token_secret_name]

bot = commands.Bot(command_prefix='-', description="haldibot.")

@bot.event
async def on_ready():

	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='hooky'))

@bot.command()
async def status(ctx, *args):
	status_switch = {
		"playing": discord.ActivityType.playing,
		"watching": discord.ActivityType.watching,
		"listening": discord.ActivityType.listening,
		"streaming": discord.ActivityType.streaming
	}
	selected_type = status_switch.get(args[0], discord.ActivityType.unknown)
	selected_name = " ".join(args[1:])
	await bot.change_presence(activity=discord.Activity(type=selected_type, name=selected_name))

@bot.command()
async def echo(ctx, *args):
	response = " ".join(args)
	await ctx.send(response)

@bot.command()
async def hello(ctx):
	message = "Hello, <@{}>!  Have a nice day.".format(str(ctx.message.author.id))
	await ctx.send(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sentiment(ctx, *args):
	message_text = await get_message(bot, ctx)
	comprehend = boto3.client('comprehend', region_name='us-west-2')
	response = comprehend.detect_sentiment(Text=message_text, LanguageCode="en")
	sentiment = response['Sentiment']
	score = int(float(response['SentimentScore'][sentiment.title()]) * 100)
	sentiment_string = f"I am {score}% sure that your tone was {sentiment}"
	await ctx.send(str(sentiment_string))

@bot.command()
async def eightball(ctx):
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
	await ctx.send(str(val))

@bot.command()
async def stonks(ctx, *args):
	token_secret_name = 'stockAPIKey'
	stock_token_response = secrets_client.get_secret_value(SecretId=token_secret_name)
	stock_token_response_dict = json.loads(stock_token_response['SecretString'])
	stock_token = stock_token_response_dict[token_secret_name]
	# Default is Slack stock, if none is specified
	# Otherwise, get the first four characters in the provided string
	symbol = "work"
	if args:
		symbol = args[0][0:4]
	url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={stock_token}"
	try:
		response = requests.get(url).json()
	except:
		await ctx.send("Couldn't find that company.")
		return
	company = response['companyName']
	company_symbol = response['symbol']
	price = response['latestPrice']
	change = round(response['change'], 2)

	color = discord.Colour.green() if change > 0 else discord.Colour.red()
	# API gives a minus sign for negative change, but no plus for positive
	# So determine which it was, and ensure we store the sign outside of the dollar sign
	# in the final output
	change_string = str(change)
	sign = "+"
	if "-" in change_string:
		sign = "-"
		change_string = change_string[1:]
	change_percent = round(response['changePercent'], 2)



	embed = discord.Embed(title="stonks!", color=color)
	embed.add_field(name="Company Name", value=f"{company} ({company_symbol})", inline=False)
	embed.add_field(name="Current Value", value=f"${price}", inline=True)
	embed.add_field(name="Change", value=f"{sign}${change_string} ({change_percent}%)", inline=True)
	if symbol == "work":
		# Only do this if slack is specified - determines the value of 2.51 owned shares
		total = round(2.51 * price, 2)
		embed.add_field(name="Value of Your Shares", value=f"${total}", inline=False)
	await ctx.send(embed=embed)


bot.run(discord_token)