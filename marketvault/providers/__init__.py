from abc import ABC, abstractclassmethod
from marketvault import log
import signal


class IProvider(ABC):
    """Base class for Provider"""

    def __init__(self, queue=None, shutdown_event=None, *args, **kwargs):
        log.install_q_logger(queue)
        self.shutdown_event = shutdown_event
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    @abstractclassmethod
    def shutdown(self, signalNumber, frame):
        """This function should contain code to handle SIGTERM signals"""
