# metrics/resources/plugins.py
"""Holds the API's for plugins and plugin updates."""
import json

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from metrics.database.models import Plugin, SpigotPlugin, PluginUpdate


class PluginsAPI(Resource):
    """API for groups of plugins"""

    @staticmethod
    def get():
        """
        Gets the plugins in the database.
        :return: The list of plugins from the database, and all their info.
        """
        updates = Plugin.objects.only('description', 'download_url').filter().to_json()
        return Response(updates, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        """
        Add a plugin to the database.
        :return: The id of the plugin in the database.
        """
        body = request.get_json()
        args = request.args

        if "spigot" in args['type'] or body['spigot_name'] is not None:
            plugin = SpigotPlugin(**body)
        else:
            plugin = Plugin(**body)

        for update in plugin.updates:
            update.server_id = get_jwt_identity()

        plugin.save()
        return {'id': str(plugin.id)}, 200


class PluginAPI(Resource):
    """API for individual plugins, specified in the request."""

    # FORMAT FOR DATES IS Y-m-D H:M:S
    @jwt_required
    def put(self, plugin_name):
        """
        Updates info for a specific plugin in the database.
        :param plugin_name: The name of the plugin being updated.
        :return: The plugin information from the db.
        """
        body = request.get_json()
        updated_doc_count = Plugin.objects.filter(name=plugin_name).update(**body)

        if updated_doc_count > 0:
            return '', 200
        else:
            return {'msg': 'No documents found under that name.'}, 404

    @jwt_required
    def delete(self, plugin_name):
        """
        Delete a specific plugin from the database.
        :param plugin_name: The plugin to delete.
        :return: A http response code.
        """
        deleted_doc_count = Plugin.objects.filter(name=plugin_name).delete()

        if deleted_doc_count > 0:
            return '', 200
        else:
            return {'msg': 'No documents found under that name.'}, 404

    @staticmethod
    def get(plugin_name):
        """
        Get info for a specific plugin from the database.
        :param plugin_name: The plugin to retrieve the info of.
        :return: The plugin information from the db.
        """
        update = Plugin.objects(name=plugin_name).first_or_404().to_json()
        return Response(update, mimetype="application/json", status=200)


class UpdatesAPI(Resource):
    """API for adding and getting specific plugins from the database."""

    @staticmethod
    def get(plugin_name):
        """
        Gets all updates from a specific plugin.
        :param plugin_name: The name of the plugin to retrieve the updates of.
        :return: The updates of the given plugin.
        """
        updates = Plugin.objects.only('updates').get_or_404(name=plugin_name)
        updates_json = json.dumps(json.loads(updates.to_json())['updates'])
        return Response(updates_json, mimetype="application/json", status=200)

    @jwt_required
    def post(self, plugin_name):
        """
        Add an update to a specific plugin.
        :param plugin_name: The name of the plugin to add an update entry for.
        :return: A http response code.
        """
        body = request.get_json()
        plugin = Plugin.objects.get(name=plugin_name)
        plugin_update = PluginUpdate(**body)
        plugin_update.server_id = get_jwt_identity()
        plugin.updates.append(plugin_update)
        plugin.save()
        return '', 200
