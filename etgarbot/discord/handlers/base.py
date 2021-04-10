from abc import ABC, abstractmethod
import typing
import string
import itertools
import discord

# - - - Typing hints - - - #
MessageScore = typing.Union[float, int, ]


class BaseCommand(ABC):

    _message: discord.Message
    score: MessageScore

    @abstractmethod
    async def message_handle(self,) -> None:
        """ Respones to the message saved in the `_message` property. It can
        be, for example, a replay, a direct message, or a reaction. """

    @abstractmethod
    def calculate_score(self,) -> MessageScore:
        """ Recives a message instance, and returns a score between 0 and 1.
        When the score is 1 (integer), it is guaranteed that the
        `message_handle` method will be called with the given message.
        When the score is 0 (integer), it is guaranteed that the
        `message_handle` method WON'T be called with the given message.
        With any values between 0 and 1, the discord bot client will
        automatically pick the message that has the top score and will call
        `message_handle` on that instance. """

    @abstractmethod
    def short_description(self,) -> str:
        """ Returns a short description that describes the current message
        handler. This is used and displayed, for example, when using the 'help'
        command. """

    @abstractmethod
    def long_description(self,) -> str:
        """ Returns a long description that describes the current message
        handler. This is used and displayed, for example, when using the 'help'
        command. """


class BaseMessageHandler(ABC):
    """ A message handler contains a group of commands that work together to serve
    similar purposes and that relay on each other. """

    def message_to_command(self,
                           message: discord.Message
                           ) -> typing.Optional[BaseCommand]:
        """ Recives a message instance, and returns a command instance that
        already contains and wraps the message instance. """


class MessageHandlerUtils:
    """ A collection of static methods that are used in different message
    handlers in the bot. """

    VALID_KEYWORDS = (
        "גדי",
        "gadi",
    )

    @classmethod
    def with_prefix(cls, message: str) -> bool:
        """ Recives the message as a string, and returns `True` if the message
        starts with the bot prefix. """

        return any(message.lower().startswith(prefix.lower() + whitespace)
                   for prefix in cls.VALID_KEYWORDS
                   for whitespace in string.whitespace)

    @classmethod
    def rearrange_words(cls, s: str) -> typing.Set[str]:
        """ Recives a string and returns an iterable that yields strings
        containing all of the possible word rearrangements in the given
        string. """

        words = s.split()
        return set(
            ' '.join(permutation)
            for permutation in itertools.permutations(words)
        )

    @classmethod
    def union_possabilities(cls, *possabilities: typing.Iterable[set]) -> set:
        return possabilities[0].union(*possabilities[1:])
