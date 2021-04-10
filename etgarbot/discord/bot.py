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
            key=lambda handler: handler.message_to_score(message)
        )

        score = handler.message_to_score(message)
        if score >= self.ScoreThreshold:
            await handler.message_handle(message)

            logger.info(
                "The '%s' handler handled (matching %d%%) the following message: '%s'",
                handler.__class__.__name__,
                int(score * 100),
                message.content,
            )
