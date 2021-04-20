from .app import MarketVault

# logger = logging.getLogger()
# logging.basicConfig()
# logger.setLevel(logging.DEBUG)

# logger.info("ASDFASDFASDFASDFASDF")


def debug():
    try:
        app = MarketVault()
        # print(f"{app.pm.plugins=}")
        # print(f"{app.settings=}")
        # print(f"{app.providers=}")
        # print(f"{dir(app.providers['coinbase'])=}")
        import time

        time.sleep(4)
        # while not app.providers['coinbase']['future'].done():
        #     # print('Still running. Sleeping 1s...')
        #     time.sleep(1)

        # print(f"{app.providers['coinbase']['future'].result()=}")
    except Exception as e:
        raise e
    finally:
        app.shutdown()
        print("CLI done")


def cli():
    debug()
