import typing
import logging
import discord

from .handlers.base import BaseMessageHandler

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

        handler: BaseMessageHandler = max(
            self.MessageHandlers,
            key=lambda handler: handler.message_to_score()
        )

        if handler.message_to_score() >= self.ScoreThreshold:
            handler.message_handle(message)
