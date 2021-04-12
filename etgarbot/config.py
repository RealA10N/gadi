import os
import logging

logger = logging.getLogger(__name__)


class Config:
    """ A class that loads the configuration files, checks if all the needed
    data is provided, and lets the module use the data in the files. """

    REQUIRED_FILES = (
        'token',
    )

    FILES_EXTENTION = '.yml'

    def __init__(self, config_folder_path: str = None):
        """ Recives the path to the configurations folder, and loads the data
        from there. If the configuration folder path isn't provided, tries
        to find the `config` folder by itself. Raises errors if the folder
        isn't found, or if critical data is missing. """

        options_for_folder = (
            config_folder_path,
            os.getcwd(),
            os.path.join(os.getcwd(), 'config'),
        )

        config_folder_path = next((
            element for element in options_for_folder
            if element is not None
            and self.is_valid_config_folder(element)),
            default=None
        )

        if config_folder_path is None:
            raise ConfigDirectoryNotFoundError(
                "Configure directory is not found or some configuration files are missing")

    @classmethod
    def is_valid_config_folder(cls, path: str) -> bool:
        """ Recives a path to a folder, and returns `True` only if the given
        path is a folder that contains the required configure files. """

        if not os.path.isdir(path):
            return False

        return all(
            os.path.isfile(os.path.join(path, file + cls.FILES_EXTENTION))
            for file in cls.REQUIRED_FILES
        )


class ConfigDirectoryNotFoundError(FileNotFoundError):
    """ Raised by the constructor of the `Config` object if the configuration
    folder isn't provided and/or not found automatically. """
