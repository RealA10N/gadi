import discord


async def replay_to_message(
        message: discord.Message,
        reply_with: str,
        *args, **kwargs,) -> None:
    """ Sends a message in the same channel with `message` as a reply to
    the given message. """

    await message.channel.send(reply_with, *args, **kwargs | {
        "reference": message,
        "mention_author": False,
    })


async def react_to_message(
        message: discord.Message,
        reaction: str,
        *args, **kwargs) -> None:
    raise NotImplementedError()


async def is_user_mod(user: discord.Member) -> bool:
    raise NotImplementedError()


async def is_admin(user: discord.Member) -> bool:
    raise NotImplementedError()


async def is_sender_mod(message: discord.Message) -> bool:
    raise NotImplementedError()


async def is_author_admin(message: discord.Message) -> bool:
    raise NotImplementedError()


async def message_remove_mentions(content: str) -> str:
    raise NotImplementedError()


async def message_remove_channel_mentions(content: str) -> str:
    raise NotImplementedError()


async def message_remove_markdown(content: str) -> str:
    raise NotImplementedError()
