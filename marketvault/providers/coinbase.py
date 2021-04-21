from marketvault.providers import IProvider
from pydantic import BaseModel
from typing import List
import logging
import sys
import time



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

        logger.info("Coinbase provider initialized")

        self.work()
    
    def work(self):
        while True:
            logger.info("Doing work...")
            logger.info(f"{self.shutdown_event.is_set()=}")
            time.sleep(5)
            if self.shutdown_event.is_set():
                break
        
        self.shutdown()
    
    def shutdown(self):
        logger.info("Shutdown called")
        sys.exit()


def run(config, *args, **kwargs):
    """
    This method provides the entrypoint used as the target for mp.Process(target=).
    It should instantiate any objects, and start the main loop of the plugin.
    """
    provider = Provider(config, *args, **kwargs)
    return True
