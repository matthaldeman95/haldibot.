async def get_message(context):
    message = context.message
    channel = context.channel
    async for elem in channel.history(limit=1, before=message):
        return elem.content

async def get_thumbnail_url(context):
    """
    Check the last 5 messages in the channel to find one with an image attachment
    Return the URL of this, or None if none is found
    """
    message = context.message
    channel = context.channel
    async for elem in channel.history(limit=5, before=message):
        if elem.attachments:
            return elem.attachments[0].url
        elif elem.embeds:
            return elem.embeds[0].thumbnail.url
    return None

async def get_attachment_link(context):
    """
    Check the last 5 messages in the channel to find one with an image attachment
    Return the URL of this, or None if none is found
    Feels like a lot of code duplication with get_thumbnail_url TODO
    """
    message = context.message
    channel = context.channel
    async for elem in channel.history(limit=5, before=message):
        if elem.embeds:
            return elem.embeds[0].url
    return None