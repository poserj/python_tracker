import yaml


def init_db():
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data['DB']
        except yaml.YAMLError as exc:
            raise yaml.YAMLError
