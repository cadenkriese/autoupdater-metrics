from .update import PluginsAPI, TestAPI, UpdatesAPI, PluginAPI


def initialize_routes(api):
    api.add_resource(PluginsAPI, "/plugins")
    api.add_resource(PluginAPI, "/plugins/<plugin_name>")
    api.add_resource(UpdatesAPI, "/plugins/<plugin_name>/updates")
    api.add_resource(TestAPI, "/test")
