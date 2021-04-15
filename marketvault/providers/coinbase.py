from marketvault.providers import IProvider
from pydantic import BaseModel


class Settings(BaseModel):
    API_KEY: str = None


class Provider(IProvider):
    def __init__(self, config):
        if type(config) is dict:
            self.settings = Settings(**config)
        else:
            self.settings = Settings()
