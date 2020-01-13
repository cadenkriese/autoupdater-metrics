# metrics/resources/routes.py
"""Initializes flask-restful routes."""
from .auth import AuthAPI
from .plugins import PluginsAPI, UpdatesAPI, PluginAPI


def initialize_routes(api):
    """Initializes flask-restful routes for the current app."""
    api.add_resource(PluginsAPI, "/updater-metrics/v1/plugins")
    api.add_resource(PluginAPI, "/updater-metrics/v1/plugins/<plugin_id>")
    api.add_resource(UpdatesAPI, "/updater-metrics/v1/plugins/<plugin_id>/updates")

    api.add_resource(AuthAPI, "/updater-metrics/v1/auth")
