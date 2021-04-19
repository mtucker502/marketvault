from .plugins import pm
from .settings import settings
from concurrent.futures import ProcessPoolExecutor
import logging
from logging import handlers
import multiprocessing_logging

import multiprocessing
multiprocessing.set_start_method('fork')  # Update default for OSX.

logger = logging.getLogger(__name__)

class MarketVault:
    def __init__(self):
        self.settings = settings
        self.setup_logging()
        multiprocessing_logging.install_mp_handler()

        self.providers = {}
        self.pm = pm

        self.executor = ProcessPoolExecutor(self.settings.get('max_workers'))
        self.load_providers()

        #FIXME: Need method to watch health of provider plugins

    def load_providers(self):
        self.logger.info("Loading provider settings")
        # We only load plugin providers for which we have configuration
        # If providers configuration is not present, just exit
        if not self.settings.get("providers"):
            self.logger.warning("No provider configuration found!")
            return None

        _PROVIDER_PREFIX = "provider_"
        for name, entrypoint in self.pm.plugins.items():
            provider_name = name.split(_PROVIDER_PREFIX)[1]
            provider_settings = self.settings["providers"].get(provider_name)


            if name.startswith(_PROVIDER_PREFIX) and provider_settings:
                provider = entrypoint.load()
                self.providers[provider_name] = dict(
                    entrypoint = provider,
                    futures = self.executor.submit(provider.run, provider_settings),
                )
                # provider#.Provider(provider_settings)
                # self.executor.submit(provider.module_name + ".run", provider_settings)
                # # self.providers[provider_name] = provider.Provider(provider_settings)
                # self.providers[provider_name] = provider#.Provider(provider_settings)
        
        #FIXME: Log on providers that are configured but not installed, (WARNING)
        #FIXME: Log providers that are installed but not configured (INFO)
    
    def setup_logging(self):
        self.logger = logger
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        #FIXME: Change log level based on settings
        # File Handler
        fh = handlers.RotatingFileHandler(self.settings.get('log_file', 'test.log'), maxBytes=1000000, backupCount=3)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Console Output
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    # FIXME: Updates to database should also update websocket IF websocket is active and there are subscribers