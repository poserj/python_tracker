import logging

import yaml
from app.logger_project import init_logger
init_logger()


def get_app_config() -> dict:
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            logging.info(data['APP'])
            return data['APP']
        except yaml.YAMLError as exc:
            logging.error("cant load data['APP']")
            raise yaml.YAMLError


def get_sec_config() -> dict:
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            logging.info(data['SECURITY'])
            return data['SECURITY']
        except yaml.YAMLError as exc:
            logging.error("Cant load data['SECURITY']")
            raise yaml.YAMLError



def init_security() -> dict:
    logging.info('init_security')
    return get_sec_config()


