async def get_message(context):
    message = context.message
    channel = context.channel
    async for elem in channel.history(limit=1, before=message):
        return elem.content
