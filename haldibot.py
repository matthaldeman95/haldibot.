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

token_secret_name = 'discordBotToken'
token_response = secrets_client.get_secret_value(SecretId=token_secret_name)
token_response_dict = json.loads(token_response['SecretString'])
discord_token = token_response_dict[token_secret_name]

bot = commands.Bot(command_prefix='-', description="haldibot.")

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
async def stonks(ctx):
	token_secret_name = 'stockAPIKey'
	stock_token_response = secrets_client.get_secret_value(SecretId=token_secret_name)
	stock_token_response_dict = json.loads(stock_token_response['SecretString'])
	stock_token = stock_token_response_dict[token_secret_name]
	url = "https://cloud.iexapis.com/stable/stock/work/quote?token=" + stock_token
	response = requests.get(url).json()
	price = response['latestPrice']
	total = 2.51 * price
	await ctx.send("$" + str(round(total, 2)))


bot.run(discord_token)