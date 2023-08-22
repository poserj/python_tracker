import yaml


def get_app_config() -> dict:
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data['APP']
        except yaml.YAMLError as exc:
            raise yaml.YAMLError


def get_sec_config() -> dict:
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data['SECURITY']
        except yaml.YAMLError as exc:
            raise yaml.YAMLError


def init_security() -> dict:
    return get_sec_config()
