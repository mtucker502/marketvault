from .plugins import pm
from .settings import settings


class MarketVault:
    def __init__(self):
        self.settings = settings
        self.providers = {}
        self.pm = pm
        self.load_providers()

    def load_providers(self):
        # We only load plugin providers for which we have configuration
        # If providers configuration is not present, just exit
        if not self.settings.get("providers"):
            return None

        _PROVIDER_PREFIX = "provider_"
        for name, entrypoint in self.pm.plugins.items():
            provider_name = name.split(_PROVIDER_PREFIX)[1]
            provider_settings = self.settings["providers"].get(provider_name)
            if name.startswith(_PROVIDER_PREFIX) and provider_settings:
                provider = entrypoint.load()
                self.providers[provider_name] = provider.Provider(provider_settings)
