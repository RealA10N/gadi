import os
import logging
import yaml

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
            and self.is_valid_config_folder(element))
        )

        if config_folder_path is None:
            raise ConfigDirectoryNotFoundError(
                "Configure directory is not found or some configuration files are missing")

        self._folder = config_folder_path
        self._content = dict()
        self.load_content()

    def load_content(self,) -> None:
        """ Opens the configuration files one by one, and loads the contents. """

        filename_to_path = lambda name: os.path.join(
            self._folder, name + self.FILES_EXTENTION)

        for filename in self.REQUIRED_FILES:
            with open(filename_to_path(filename), encoding='utf8') as file:
                self._content[filename] = yaml.full_load(file)

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

    def get(self, *args):
        """ Recives a combination of strings that represent a configuration,
        and returns the configuration data. If the configuration is not
        found, a KeyError is thrown. """

        data = self._content
        for arg in args:
            data = data[arg]
        return data

    def get_safely(self, *args, default=None):
        """ Recives a combination of strings that represent a configuration,
        and returns the configuration data. If the a configuration is not
        found, returns the deafult value. """

        try:
            self.get(*args)
        except KeyError:
            return default


class ConfigDirectoryNotFoundError(FileNotFoundError):
    """ Raised by the constructor of the `Config` object if the configuration
    folder isn't provided and/or not found automatically. """
