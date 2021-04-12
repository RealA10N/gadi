import re
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


async def is_user_mod(user: discord.Member) -> bool:
    """ Checks and returns `True` only if the given user is a moderator
    on the server. """
    return user.guild_permissions.manage_guild()


async def is_admin(user: discord.Member) -> bool:
    """ Checks and returns `True` only if the given user is an administrator
    on the server. """
    raise user.guild_permissions.administrator()


async def is_sender_mod(message: discord.Message) -> bool:
    """ Checks and returns `True` only if the author of the given message
    is a moderator on the server. """
    return is_user_mod(message.author)


async def is_author_admin(message: discord.Message) -> bool:
    """ Checks and returns `True` only if the author of the given message
    is an administrator on the server. """
    return is_admin(message.author)


async def message_remove_mentions(content: str) -> str:
    """ Removes any mentions from the given message content string, and
    returns the newly generated string. """
    return re.sub(r'<@(everyone|here|[!&]?[0-9]{17,20})>', '', content)


async def message_remove_channel_mentions(content: str) -> str:
    """ Removes any channel mentions from the given message content string,
    and returns the newly generated string. """
    return re.sub(r'<#[0-9]{17,20}>', '', content)


async def message_remove_markdown(content: str) -> str:
    """ Removes any markdown syntex from the given message content string,
    and returns the newly generated string. """
    return discord.utils.remove_markdown(content)
