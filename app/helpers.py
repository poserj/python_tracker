import yaml


def init_app():
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data['APP']
        except yaml.YAMLError as exc:
            raise yaml.YAMLError