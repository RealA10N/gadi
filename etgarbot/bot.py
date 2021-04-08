import logging
import discord

logger = logging.getLogger(__name__)


class EtgarBot(discord.Client):

    async def on_ready(self,):
        """ Called when the bot finishes to boot up. """
        logger.info("Successfully Logged with user '%s'", self.user)
