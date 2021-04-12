import typing
import logging
import json
import asyncio
import atexit
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# - - - Typing hints - - - #
JsonSuppored = typing.Union[None, dict, list, int, float, bool, ]
UnixTimestamp = float


class DynamicData:

    """ The bot uses a couple of json files that store data.
    Storing this data always in memory can be bad, especially at night
    for example, when usually no one uses the bot.
    When accessing json data files using this object, the data will be
    loaded to memory and will stay in memory for X seconds. If the data
    isn't accessed another time in those X seconds, the data will be saved
    to local storage and will be deleted from the memory, to save up
    RAM. """

    def __init__(self,
                 filepath: str,
                 hold_for: int = 15 * 60,
                 check_every: int = 60,
                 save_atexit: bool = True,
                 default_data: typing.Union[dict, list] = None,
                 ):
        """ Creates a dynamic data instance. When calling the constructor,
        the file is not actually read.
        `hold_for` is the number of seconds that the data will be stored
        in the memory before moving it to the local storage. By default,
        the data will be stored in the memory for 15 seconds.
        `check_every` determines how frequently the instance preforms checks
        for last updated time. `check_every` is the amount of seconds between
        checks, and it's set to 1 minute by default. """

        if (  # Checks if default_data is valid
            not default_data is None
            and not isinstance(default_data, (list, dict))
        ):
            raise TypeError("Default data should be a dict or a list")

        self._filepath = filepath
        self._hold_for = hold_for
        self._check_every = check_every
        self._default_data = default_data

        self._data: JsonSuppored = DataNotLoaded()
        self._last_accessed: UnixTimestamp = None

        if save_atexit:
            atexit.register(self.throw_data)

    def data(self,) -> JsonSuppored:
        """ Returns the data that is saved in the file.
        Loads the file if needed. """

        if isinstance(self._data, DataNotLoaded):
            self.load_data()

        # Update last accessed timestamp
        now = datetime.now().timestamp()
        first_time = self._last_accessed is None
        self._last_accessed = now

        if first_time:
            asyncio.create_task(self._update_check_loop())

        return self._data

    def load_data(self,) -> None:
        """ When called, loads the file from the storage (overwrites already
        loaded data if needed). """

        if os.path.isfile(self._filepath):
            with open(self._filepath) as file:
                self._data = json.load(file,)

            logger.debug("Loaded dynamic data: %s", self._filepath)

        else:   # If file doesn't exist
            logger.warning(
                "File not found while loading dynamic data: %s",
                self._filepath
            )

            self.load_default_data()

    def load_default_data(self,) -> None:
        """ Loads the default data provided to the constructor as the dynamic
        data of this instance. """

        if self._default_data is None:
            raise ValueError("Dynamic default data is not provided")

        self._data = self._default_data

        logger.warning(
            "Loaded default data to dynamic data instance: %s", self._filepath)

    def throw_data(self,) -> None:
        """ When called, deletes the data file from the memory, and saves it
        into the storage. """

        if isinstance(self._data, DataNotLoaded):
            return  # if data is already not loaded, does nothing silently.

        with open(self._filepath, 'w') as file:
            json.dump(self._data, file)

        self._data = DataNotLoaded()

        logger.debug("Saved dynamic data: %s", self._filepath)

    async def _update_check_loop(self,):
        """ A loop that runs while the file is loaded. Sleeps must of the time,
        but once in a while wakes up and checks if the file is old enough. If
        it is (and it haven't been accessed), the data is throwen. """

        while self._last_accessed is not None:
            await asyncio.sleep(self._check_every)

            now = datetime.now().timestamp()
            delta = now - self._last_accessed

            if delta >= self._hold_for:
                self.throw_data()
                self._last_accessed = None


# - - - Other objects - - - #


class DataNotLoaded:
    """ Stored as a placeholder (used kind of as a `None`) in the implementation
    of the DynamicData object. """
