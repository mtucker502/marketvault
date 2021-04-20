from abc import ABC, abstractclassmethod
from marketvault import log


class IProvider(ABC):
    """Base class for Provider"""

    def __init__(self, queue=None, *args, **kwargs):
        log.install_q_logger(queue)
