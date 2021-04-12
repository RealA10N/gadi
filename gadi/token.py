import logging

logger = logging.getLogger(__name__)


VALID_TOKEN_FILE_NAMES = (
    "token", "token.txt",
    "credential", "credential.txt",
    "credentials", "credentials.txt",
)


def get_token():
    """ Checks if a credentials / config file is provided.
    If such file is not located, requests the token from the user
    directly using the console. """

    for filename in VALID_TOKEN_FILE_NAMES:

        try:
            with open(filename, 'r') as file:
                token = file.read().strip()
                logger.info(
                    "Loaded discord bot token from the '%s' file", filename)
                return token

        except FileNotFoundError:
            # If current file name is not found,
            # continue to check other file names
            continue

    # If could not find a file for the token, returns None.
    logger.error(
        "A file with a discord token (e.g. 'token.txt') wasn't located.")
    return None
