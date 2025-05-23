from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
load_dotenv()

class Text2VideoRequest(BaseModel):
    prompt: Optional[str] = None
    fps: Optional[int] = 129


class Image2VideoRequest(BaseModel):
    image: Optional[str] = None
    prompt: Optional[str] = None
    fps: Optional[int] = 129

class EndpointConfig(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    endpoint: Optional[str] = None
    url: Optional[str] = None

class ConfigManager(BaseModel):
    environment: Optional[str] = None
    configs: dict[str, EndpointConfig] = {}
    host_ip: Optional[str] = None

    def __init__(self, environment: str):
        super().__init__()
        self.environment = os.getenv("environment")
        self.host_ip = os.getenv("HOST_IP")
        self.configs = {}

    def get_config(self, value: str) -> EndpointConfig:
        if value not in self.configs:
            self._set_config(value)
        return self.configs[value]

    def _set_config(self, value: str) -> None:
        variable_path_string = f"{self.environment}_{value}_"
        self.configs[value] = EndpointConfig(
            host=os.getenv(f"{variable_path_string}host"),
            port=os.getenv(f"{variable_path_string}port"),
            endpoint=os.getenv(f"{variable_path_string}endpoint"),
            url=os.getenv(f"{variable_path_string}url"),
        )