"""Настройки."""

from configparser import ConfigParser
from pydantic import BaseModel


class Config(BaseModel):
    """Конфиг сервера."""
    host: str
    port: int


config_parser: ConfigParser = ConfigParser()
config_parser.read('backend/config.ini')

config: Config = Config(
    host=config_parser.get('server', 'host'),
    port=config_parser.get('server', 'port'),
)



