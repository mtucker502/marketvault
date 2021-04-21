from .log import logger_thread, LOGGING_CONFIG
from .plugins import pm
from .settings import settings
from .log import logger_thread, LOGGING_CONFIG
import logging
import logging.handlers
import logging.config
import multiprocessing as mp
import signal
import sys
import threading
import time
from typing import List



class MarketVault:
    def __init__(self):
        self.settings = settings
        self.setup_logging()
        self._stop = False
        self.setup_sighandlers()
        self.shutdown_event = mp.Event()
        self.pm = pm
        self.workers: List[mp.Process] = []
        self.load_providers()
        
        self.main_loop()


    def shutdown(self):
        """Gracefully shutdown all processes, threads and IO"""

        # Shutdown Providers
        self.logger.info("Setting shutdown event")
        self.shutdown_event.set()
        time.sleep(10)
        for worker in self.workers:
            if worker.is_alive():
                try:
                    self.logger.info(f"Sending SIGTERM to {worker.name} (PID {worker.pid})")
                    worker.terminate()
                    self.logger.info(f"Successfully shutdown {worker.name}")
                except mp.TimeoutError:
                    self.logger.info(f"Timedout waiting for {worker.name} (PID {worker.pid}) to exit")
                    self.logger.info(f"Sending SIGKILL to {worker.name} (PID {worker.pid})")
                    worker.kill()
            else:
                self.logger.info(f"Worker {worker.name} is no longer running")

        # Shutdown the logging thread
        self.logger.info("Shutting down the logging thread")
        self.log_queue.put(None)
        self.lt.join()
        self.logger.info("Logging thread has shutdown")

        sys.exit()


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
                    name=provider_name,
                    args=(settings,),
                    kwargs=dict(
                        queue=self.log_queue,
                        shutdown_event=self.shutdown_event,
                    ),
                )
                self.workers.append(worker)
                worker.start()
                self.logger.info(f"Provider plugin {provider_name} started in PID {worker.pid}")

        # FIXME: Log on providers that are configured but not installed, (WARNING)
        # FIXME: Log providers that are installed but not configured (INFO)


    def setup_logging(self):
        logging.config.dictConfig(LOGGING_CONFIG)
        self.log_queue = mp.Manager().Queue(-1)
        self.lt = threading.Thread(target=logger_thread, args=(self.log_queue,))
        self.lt.start()
        self.logger = logging.getLogger(__name__)


    def _sigHandler(self, signalNumber, frame):
        self.logger.info(f"Signal {signalNumber} received. Calling shutdown")
        self._stop = True
    

    def setup_sighandlers(self):
        # signal.signal(signal.SIGTERM, self._sigHandler)  #FIXME: enable this after we have better error control
        signal.signal(signal.SIGINT, self._sigHandler)  #FIXME: add counter here so we have to interrupt twice


    def main_loop(self):
        while True:
            # TODO: Monitor health of workers
            self.logger.info("Main loop. Sleeping 5s")
            time.sleep(10)


            if self._stop:
                self.logger.info("Exiting main loop")
                break
        
        self.shutdown()

