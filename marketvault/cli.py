from .app import MarketVault


app = MarketVault()


def debug():
    print(f"{app.pm.plugins=}")
    print(f"{app.settings=}")
    print(f"{app.providers=}")
    print(f"{app.providers['coinbase'].settings=}")


def cli():
    debug()
