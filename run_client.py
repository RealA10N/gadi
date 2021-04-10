import logging
from etgarbot import EtgarBot
from etgarbot.token import get_token


def config_logging():
    logger = logging.getLogger('etgarbot')
    stream = logging.StreamHandler()

    logger.setLevel(logging.INFO)
    stream.setLevel(logging.INFO)

    logger.addHandler(stream)


if __name__ == "__main__":
    config_logging()
    token = get_token()
    if token is not None:
        EtgarBot().run(token)
