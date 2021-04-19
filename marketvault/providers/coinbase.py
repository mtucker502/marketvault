from marketvault.providers import IProvider
from pydantic import BaseModel
from typing import List
import time
import logging


logger = logging.getLogger(__name__)

class Settings(BaseModel):
    api_key: str = None
    symbols: List = None


class Provider(IProvider):
    def __init__(self, config):
        if type(config) is dict:
            self.settings = Settings(**config)
        else:
            self.settings = Settings()

def run(config):
    provider = Provider(config)
    for _ in range(5):
        logger.info('coinbase_Test')
        time.sleep(1)
    return "COINBASE FINISHED"
    