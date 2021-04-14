import logging
from gadi import GadiBot, Config


def configure_logging():
    logger = logging.getLogger('gadi')
    stream = logging.StreamHandler()

    logger.setLevel(logging.INFO)
    stream.setLevel(logging.INFO)

    logger.addHandler(stream)

    return logger


def run_client(logger: logging.Logger = logging.getLogger()):
    config = Config()
    token = config.get_safely('token')

    if token is None:
        logger.error(
            'A Discord bot token is not provided. Paste your token inside ./config/token.yml')

    else:
        logger.info('Loaded Discord bot token from ./config/token.yml')
        GadiBot(config=config).run(token)


if __name__ == "__main__":
    logger = configure_logging()
    run_client(logger)
