import logging
import logging.config
import logging.handlers

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detailed",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "marketvault.log",
            "mode": "w",
            "formatter": "detailed",
        },
        "errors": {
            "class": "logging.FileHandler",
            "filename": "marketvault-errors.log",
            "mode": "w",
            "level": "ERROR",
            "formatter": "detailed",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file", "errors"]},
}


def logger_thread(q):
    # log_configurer(q)
    while True:
        record = q.get()
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)


def install_q_logger(q):
    """Configures the root logger to be used in plugin multiprocesses"""
    qh = logging.handlers.QueueHandler(q)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(qh)


# if __name__ == '__main__':
#     q = Queue()

#     for i in range(5):
#         wp = Process(target=worker_process, name='worker %d' % (i + 1), args=(q,))
#         workers.append(wp)
#         wp.start()
#     logging.config.dictConfig(d)
#     lp = threading.Thread(target=logger_thread, args=(q,))
#     lp.start()
#     # At this point, the main process could do some useful work of its own
#     # Once it's done that, it can wait for the workers to terminate...
#     for wp in workers:
#         wp.join()
#     # And now tell the logging thread to finish up, too
#     q.put(None)
#     lp.join()
