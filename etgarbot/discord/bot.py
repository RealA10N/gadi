import typing
import logging
import discord

from .handlers.base import BaseMessageHandler, BaseCommand

logger = logging.getLogger(__name__)


class EtgarBot(discord.Client):

    MessageHandlers: typing.Tuple[BaseMessageHandler] = (
        # Slowly, handlers will add up here!
    )

    ScoreThreshold = 0.7

    async def on_ready(self,) -> None:
        """ Called when the bot finishes to boot up. """
        logger.info("Successfully Logged in: %s", self.user)

    async def on_message(self, message: discord.Message) -> None:
        """ Called by the `discord` module when a message websocket is
        received. """

        if message.author == self.user:
            return  # If message sent by the bot itself, exits the function.

        command: BaseCommand = max((
            handler.message_to_command(message)
            for handler in self.MessageHandlers
        ),
            key=lambda command: command.score
        )

        if command.score >= self.ScoreThreshold:
            await command.message_handle()

            logger.info(
                "The '%s' command class (matching %d%%) handled the following message: '%s'",
                command.__class__.__name__,
                int(command.score * 100),
                message.content,
            )
