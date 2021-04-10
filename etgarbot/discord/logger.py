import typing
import logging
import asyncio
import discord


class DiscordLoggingChannel(logging.StreamHandler):

    def __init__(self,
                 channel: discord.TextChannel = None,
                 wait_for: int = 10):
        """ Creates a new logging stream handler that will log messages to 
        specified discord text channel. The logger squashes a couple of
        logged messages together to avoid spamming with multiple messages in
        every second. The `wait_for` tells the logger how much seconds
        it should wait between each message that is sent (by default, sends
        messages every 10 seconds). """
        super().__init__()

        self._channel = channel
        self._pending_records = list()
        self._wait_for = wait_for

        # Start running the logging loop
        asyncio.create_task(self.__logging_loop())

    def set_logging_channel(self,
                            channel: discord.TextChannel
                            ) -> None:
        """ Saves the given channel as the channel that will be used
        to display the bot log. """
        self._channel = channel

    def remove_logging_channel(self,) -> None:
        """ Removes the saved logging channel, and stops sending the bot log
        to discord channel. """
        self.set_logging_channel(None)

    def emit(self, record):
        """ Called by the logging module when a message is logged.
        Adds the message to the `pending_records` list. """
        self._pending_records.append(record)

    # - - - Private & Protected methods - - - #

    def _send_pending_records(self,):
        """ If a discord channel is provided, sends the pending log messages. """

        if self._channel is not None:
            message = self._generate_message(self._pending_records)
            self._channel.send(message)

    def _generate_message(self, records: typing.List[logging.LogRecord]) -> str:
        """ Generates a single string representing the given log records. """

        content = '\n'.join([
            self.format(record)
            for record in records
        ])

        return f'```\n{content}\n```'

    async def __logging_loop(self,):
        """ The logging loop. Loops infinitely, and sends a message to the
        discord log channel when needed. """

        while True:
            await asyncio.sleep(self._wait_for)

            if self._pending_records:
                self._send_pending_records()
                self._pending_records = list()   # Clear the pending records list
