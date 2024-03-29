import os
from loguru import logger
from utilities.data_models import EndpointConfig, ConfigManager
from dotenv import load_dotenv

load_dotenv()


class EndpointConfigManager(ConfigManager):
    def __init__(self):
        super().__init__()
        self.set_configs()

        self.all_config = self.set_all_config()

    def set_configs(self):
        self.lab = self.get_config('lab')
        self.lab1 = self.get_config('lab1')
        self.lab2 = self.get_config('lab2')
        self.lab3 = self.get_config('lab3')
        self.lab4 = self.get_config('lab4')
        self.lab5 = self.get_config('lab5')
        self.lab6 = self.get_config('lab6')
        self.lab7 = self.get_config('lab7')
        self.lab8 = self.get_config('lab8')
        self.lab9 = self.get_config('lab9')

    def set_all_config(self):
        self.all_config = {}
        for key, value in os.environ.items():
            self.all_config[key] = value
        return self.all_config

    def get_url(self, host, port, endpoint):
        return f"http://{host}:{port}{endpoint}"

    def get_config(self, value: str):
        logger.debug(f"Getting {value} config")
        host = handle_error(os.getenv(f"{self.environment}_{value}_host"))
        port = handle_error(os.getenv(f"{self.environment}_{value}_port"))
        endpoint = handle_error(os.getenv(f"{self.environment}_{value}_endpoint"))

        config_map = {"host": host, "port": port, "endpoint": endpoint}

        config_map["url"] = self.get_url(**config_map)
        logger.debug(config_map)
        return EndpointConfig(**config_map)

    def set_item(self, key, value):
        logger.debug(f"Setting {key} to {value}")
        value = os.getenv(f"{self.environment}_{value}")
        self.__setattr__(key, value)


def handle_error(value):
    if value is None:
        raise ValueError(f"value cannot be None:\n{value}")
    else:
        return value


def getEndpointConfigManager():
    return EndpointConfigManager()


def main():
    return getEndpointConfigManager()


if __name__ == "__main__":
    manager = main()
    logger.debug("lab - {manager.lab}")
    logger.debug("lab1 - {manager.lab1}")
    logger.debug("lab2 - {manager.lab2}")
    logger.debug("lab3 - {manager.lab3}")
    logger.debug("lab4 - {manager.lab4}")
    logger.debug("lab5 - {manager.lab5}")
    logger.debug("lab6 - {manager.lab6}")
    logger.debug("lab7 - {manager.lab7}")
    logger.debug("lab8 - {manager.lab8}")
    logger.debug("lab9 - {manager.lab9}")
