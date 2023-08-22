import logging

from app.helpers import get_app_config


def init_logger():
    conf = get_app_config()
    logging.basicConfig(
        level=logging.INFO,
        filename=conf["LOG_FILE"],
        filemode="w",
        format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(levelname)s  %(message)s",
    )
