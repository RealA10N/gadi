import logging
from gadi import GadiBot
from gadi.token import get_token


def config_logging():
    logger = logging.getLogger('gadi')
    stream = logging.StreamHandler()

    logger.setLevel(logging.INFO)
    stream.setLevel(logging.INFO)

    logger.addHandler(stream)


if __name__ == "__main__":
    config_logging()
    token = get_token()
    if token is not None:
        GadiBot().run(token)
