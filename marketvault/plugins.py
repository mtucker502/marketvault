import pkg_resources


class PluginManager:
    def __init__(self):
        self.plugins = self.get_plugins()

    @staticmethod
    def get_plugins():
        discovered_plugins = {
            entry_point.name: entry_point
            # entry_point.name: entry_point.load()
            for entry_point in pkg_resources.iter_entry_points("marketvault.plugins")
        }
        return discovered_plugins


pm = PluginManager()
