#!/home/matthew/haldibot/venv
import sys
import discord
from discord.channel import Channel
from discord.ext.commands import Bot

if len(sys.argv) != 3:
    print("Need to supply more arguments.")
    sys.exit(-1)
channel_id = sys.argv[1]
channel = discord.Object(id=channel_id)

client = Bot(description="haldibot.", command_prefix="-", pm_help = False)
message = sys.argv[2]
print(sys.argv)

@client.event
async def on_ready():
    channel = discord.Object(id=channel_id)
    return await client.send_message(channel, message)


if __name__ == "__main__":
    
    with open('discord.txt') as infile:
        token = infile.read()

    client.run(token)
    client.send_message(channel, "this is a test!")
    client.close()