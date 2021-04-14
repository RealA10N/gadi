from abc import ABC, abstractmethod
import typing
import itertools
import re
import discord

import gadi.utils as utils
from ...config import Config

# - - - Typing hints - - - #
MessageScore = typing.Union[float, int, ]


class BaseCommand(ABC):

    _message: discord.Message
    score: MessageScore

    VALID_KEYWORDS = (
        'גדי',
        'gadi',
    )

    def __init__(self, message: discord.Message, config: Config):
        self._message = message
        self._config = config
        self.score = self.calculate_score()

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

    def compare_score(self,
                      compare_to: str,
                      require_keyword: typing.Union[bool, str] = 'prefix',
                      allow_word_rearrange: bool = False,
                      case_sensitive: bool = False,
                      ignore_markdown: bool = True,
                      ignore_mentions: bool = True,
                      ignore_channel_mentions: bool = True,
                      ignore_whitespaces: bool = True,
                      ) -> MessageScore:
        """ Returns a floating score between 0 and 1 that indicates the how
        similar the message stored in the instance and the given one are. (0 - 
        not similar at all, 1 - the same).

        Arguments:
        -   `compare_to`: The string that is compared against the one that is
            stored in the current instance.
        -   `require_keyword`: Can be `True`, `False`, or the string `'prefix'`.
            If `True` - requires that the bot keyword will appear in the message.
            If `False` - calculates the score while ignoring keywords.
            If `'prefix'` - requires at a keyword at the beggining of the
            command.
        -   `allow_word_rearrange`: A boolean value. If `True`, checks all
            possible rearrangements of words in the `compare_to` string that
            takes the highest score. If `False`, only compares the given string.
        """

        message = self._message.content

        if ignore_markdown:
            message = discord.utils.remove_markdown(message)

        if ignore_mentions:
            message = re.sub(
                r'<@(everyone|here|[!&]?[0-9]{17,20})>', '', message)

        if ignore_channel_mentions:
            message = re.sub(r'<#[0-9]{17,20}>', '', message)

        # Remove duplicate whitespaces
        if ignore_whitespaces:
            message = ' '.join(message.split())

        # Handeling the `case_sensative` argument

        if not case_sensitive:
            # If not case sensitive, converts every string involved in the
            # compersation to lower case
            message = message.lower()
            compare_to = compare_to.lower()

        words_to_compare = tuple(compare_to.split())
        permutations = {words_to_compare}

        # Handeling the `allow_word_rearrange` argument

        if allow_word_rearrange:
            permutations = {
                permutation
                for permutation in itertools.permutations(words_to_compare)
            }

        # Handeling the `require_keyword` argument

        if require_keyword is True:
            permutations = utils.union_permutation_sets(*[
                utils.add_to_permutations(permutations, keyword)
                for keyword in self.VALID_KEYWORDS
            ])

        elif require_keyword == 'prefix':
            permutations = {
                [keyword] + permutation
                for keyword in self.VALID_KEYWORDS
                for permutation in permutations
            }

        return max(
            utils.levenshtein_score(message, ' '.join(permutation))
            for permutation in permutations
        )


class BaseMessageHandler(ABC):
    """ A message handler contains a group of commands that work together to serve
    similar purposes and that relay on each other. """

    COMMANDS: tuple     # will contain class objects (not instances).

    def __init__(self, config: Config):
        self._config = config

    def message_to_command(self,
                           message: discord.Message
                           ) -> typing.Optional[BaseCommand]:
        """ Recives a message instance, and returns a command instance that
        already contains and wraps the message instance. Returns the command
        that best matches the message. """

        return max((
            Command(message, self._config)
            for Command in self.COMMANDS
        ),
            key=lambda command: command.score,
        )
