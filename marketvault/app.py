from .plugins import pm
from .settings import settings
import multiprocessing
import logging
import logging.handlers
import logging.config
import threading
from .log import logger_thread, LOGGING_CONFIG
import multiprocessing as mp


class MarketVault:
    def __init__(self):
        self.settings = settings
        self.setup_logging()

        self.pm = pm
        # self.executor = ProcessPoolExecutor(self.settings.get('max_workers'))
        self.pool = mp.Pool()
        self.workers = []
        self.load_providers()

        # TODO: Monitor health of workers

    def shutdown(self):
        # Stop the logging thread
        self.log_queue.put(None)
        self.lt.join()

        # TODO: Providers
        # TODO: SHUTDOWN PROVIDERS

    def load_providers(self):
        """Providers will run as a subprocess. Other plugins may be treated as threads or called in separately"""

        _PROVIDER_PREFIX = "provider_"

        self.logger.debug("Loading providers")
        self.providers = {}

        # If providers configuration is not present, just exit
        if not self.settings.get("providers"):
            self.logger.info("No provider configuration found!")
            return None

        for name, entrypoint in self.pm.plugins.items():
            self.logger.debug(f"Found plugin {name} at {entrypoint.module_name}")

            provider_name = name.split(_PROVIDER_PREFIX)[1]
            provider_settings = self.settings["providers"].get(provider_name)

            # We only load plugin providers for which we have configuration
            if name.startswith(_PROVIDER_PREFIX) and provider_settings:
                provider_name = name.split(_PROVIDER_PREFIX)[1]
                provider = entrypoint.load()
                worker = mp.Process(
                    target=provider.run,
                    args=(settings,),
                    kwargs=dict(queue=self.log_queue),
                )
                self.workers.append(worker)
                worker.start()

        # FIXME: Log on providers that are configured but not installed, (WARNING)
        # FIXME: Log providers that are installed but not configured (INFO)

    def setup_logging(self):

        logging.config.dictConfig(LOGGING_CONFIG)
        self.log_queue = multiprocessing.Manager().Queue(-1)
        self.lt = threading.Thread(target=logger_thread, args=(self.log_queue,))
        self.lt.start()
        self.logger = logging.getLogger(__name__)
