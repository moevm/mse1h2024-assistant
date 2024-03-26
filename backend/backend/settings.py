"""Настройки."""

from configparser import ConfigParser
from pydantic import BaseModel


class Config(BaseModel):
    """Конфиг сервера."""
    host: str
    port: int


class ConfigWrapper:
    """Конфиг."""
    def __init__(self, path: str):
        """Конструктор."""
        self._config_wrapper: ConfigParser = ConfigParser()
        self._config_wrapper.read(path)
        self._config: Config = Config(
            host=self._config_wrapper.get('server', 'host'),
            port=self._config_wrapper.get('server', 'port'),
        )

    @property
    def config(self) -> Config:
        return self._config


def config_func(path: str) -> Config:
    return ConfigWrapper(path).config
