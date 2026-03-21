import tomllib

class Config:
    def __init__(self, config: dict):
        self.config = config


@staticmethod
def load_config(config_path: str = "app/toml/service-config.local.toml") -> Config:
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    return Config(config)

config = load_config()
