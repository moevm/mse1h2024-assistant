"""Настройки."""
import os
from configparser import ConfigParser
from pydantic import BaseModel


class Config(BaseModel):
    """Конфиг сервера."""
    host: str
    port: int
    ollama_url: str
    current_model: str
    translation_service: str
    translation_language: str
    translation_length_limit: int


class ConfigWrapper:
    """Конфиг."""
    def __init__(self, path: str):
        """Конструктор."""
        self._config_wrapper: ConfigParser = ConfigParser()
        self._config_wrapper.read(path)
        self._config: Config = Config(
            host=self._config_wrapper.get('server', 'host'),
            port=self._config_wrapper.get('server', 'port'),
            ollama_url=self._config_wrapper.get('model', 'url'),
            current_model=self._config_wrapper.get('model', 'name'),
            translation_service=self._config_wrapper.get('translation', 'service'),
            translation_language=self._config_wrapper.get('translation', 'language'),
            translation_length_limit=self._config_wrapper.get('translation', 'length_limit'),
        )

    @property
    def config(self) -> Config:
        return self._config


config: Config = ConfigWrapper(os.path.join(os.path.dirname(__file__), 'config.ini')).config
