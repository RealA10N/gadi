import typing
from abc import ABC
import discord
import string

# - - - Typing hints - - - #
MessageScore = typing.Union[float, int, ]


class BaseMessageHandler(ABC):

    async def message_handle(self, message: discord.Message) -> None:
        """ Recives a message instance and handles it (for example, with
        another response message from the bot). """

    def message_to_score(self, message: discord.Message) -> MessageScore:
        """ Recives a message instance, and returns a score between 0 and 1.
        When the score is 1 (integer), it is guaranteed that the
        `message_handle` method will be called with the given message.
        When the score is 0 (integer), it is guaranteed that the
        `message_handle` method WON'T be called with the given message.
        With any values between 0 and 1, the discord bot client will
        automatically pick the message that has the top score and will call
        `message_handle` on that instance. """

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

    VALID_KEYWORDS = (
        "גדי",
        "gadi",
    )

    @classmethod
    def highest_score(cls,
                      message: str,
                      possabilities: typing.Iterable[str]
                      ) -> MessageScore:
        """ Compares all given possabilities to the given message and returns
        the highest comperesent score. Replaces '{keyword}' in each possibility
        with each valid keyword. """

        # Replace '{keyword}' with valid keywords
        possabilities = set(
            possability.replace('{keyword}', keyword)
            for keyword in cls.VALID_KEYWORDS
            for possability in possabilities
        )

        # Returns highest matching score
        return max(
            cls.levenshtein_score(message, possability)
            for possability in possabilities
        )

    @classmethod
    def with_prefix(cls, message: str) -> bool:
        """ Recives the message as a string, and returns `True` if the message
        starts with the bot prefix. """

        return any(message.lower().startswith(prefix.lower() + whitespace)
                   for prefix in cls.VALID_KEYWORDS
                   for whitespace in string.whitespace)

    @classmethod
    def levenshtein_distance(cls, s1: str, s2: str) -> int:
        """ Returns the edit distance between the two given strings. """

        if min(len(s1), len(s2)) == 0:
            return max(len(s1), len(s2))

        previous_row = range(len(s2) + 1)  # The 'zero' row

        for i, c1 in enumerate(s1):
            current_row = [i + 1]

            for j, c2 in enumerate(s2):

                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)

                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return current_row[-1]

    @classmethod
    def levenshtein_score(cls, s1: str, s2: str) -> MessageScore:
        """ Returns a floating number between 0 and 1. If the number is 0,
        The two given strings are totally different. However, if the returned
        number is 1, the two given strings the the same. """

        max_distance = max(len(s1), len(s2))
        if max_distance == 0:
            # Special case: if both strings are empty (length zero).
            return 0

        distance = cls.levenshtein_distance(s1, s2)
        return (max_distance - distance) / max_distance
