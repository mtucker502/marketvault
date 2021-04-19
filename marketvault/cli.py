from .app import MarketVault
import logging

app = MarketVault()

logger = logging.getLogger(__name__)

def debug():
    print(f"{app.pm.plugins=}")
    print(f"{app.settings=}")
    print(f"{app.providers=}")
    print(f"{dir(app.providers['coinbase'])=}")
    # print(f"{app.providers['coinbase'].settings=}")
    # print(f"{dir(app.providers['coinbase']['futures'])=}")
    import time
    while not app.providers['coinbase']['futures'].done():
        print('Still running. Sleeping 1s...')
        time.sleep(1)
    
    print(f"{app.providers['coinbase']['futures'].result()=}")
    
    print('CLI done')

def cli():
    debug()
