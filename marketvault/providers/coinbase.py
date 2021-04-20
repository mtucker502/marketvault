from marketvault.providers import IProvider  # , Provider
from pydantic import BaseModel
from typing import List
import logging


logger = logging.getLogger(__name__)


class Settings(BaseModel):
    api_key: str = None
    symbols: List = None


class Provider(IProvider):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(config) is dict:
            self.settings = Settings(**config)
        else:
            self.settings = Settings()

        logger.info("Coinbase Provider Logger Test")


def run(config, *args, **kwargs):
    provider = Provider(config, *args, **kwargs)
    return True
