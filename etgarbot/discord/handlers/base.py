import typing
from abc import ABC
import discord
import string

# - - - Typing hints - - - #
MessageScore = typing.Union[float, int, ]


class BaseMessageHandler(ABC):

    async def message_to_score(self, message: discord.Message) -> MessageScore:
        """ Recives a message instance, and returns a score between 0 and 1.
        When the score is 1 (integer), it is guaranteed that the
        `message_handle` method will be called with the given message.
        When the score is 0 (integer), it is guaranteed that the
        `message_handle` method WON'T be called with the given message.
        With any values between 0 and 1, the discord bot client will
        automatically pick the message that has the top score and will call
        `message_handle` on that instance. """

    async def message_handle(self, message: discord.Message) -> None:
        """ Recives a message instance and handles it (for example, with
        another response message from the bot). """

    def short_description(self,) -> str:
        """ Returns a short description that describes the current message
        handler. This is used and displayed, for example, when using the 'help'
        command. """

    def long_description(self,) -> str:
        """ Returns a long description that describes the current message
        handler. This is used and displayed, for example, when using the 'help'
        command. """


class MessageHandlerUtils:
    """ A collection of static methods that are used in different message
    handlers in the bot. """

    VALID_PREFIXES = (
        "גדי",
        "gadi",
    )

    @classmethod
    def with_prefix(cls, message: str) -> bool:
        """ Recives the message as a string, and returns `True` if the message
        starts with the bot prefix. """

        return any(message.lower().startswith(prefix.lower() + whitespace)
                   for prefix in cls.VALID_PREFIXES
                   for whitespace in string.whitespace)
