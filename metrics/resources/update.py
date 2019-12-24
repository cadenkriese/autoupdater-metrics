import uuid
from datetime import datetime

from flask import Response, request

from metrics.database.models import Plugin, SpigotPlugin, PluginUpdate, PluginUpdateVersion
from flask_restful import Resource


class PluginsAPI(Resource):
    def get(self):
        updates = Plugin.objects.filter().to_json()
        return Response(updates, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        args = request.args

        if "spigot" in args['type']:
            plugin = SpigotPlugin(**body)
        else:
            plugin = Plugin(**body)

        plugin.save()
        return {'id': str(plugin.id)}, 200


class PluginAPI(Resource):
    # FORMAT FOR DATES IS Y-m-D H:M:S
    def put(self, plugin_name):
        body = request.get_json()
        Plugin.objects.filter(name=plugin_name).update(**body)

        return '', 200

    def delete(self, plugin_name):
        Plugin.objects.filter(name=plugin_name).delete()
        return '', 200

    def get(self, plugin_name):
        update = Plugin.objects(name=plugin_name).first_or_404().to_json()
        return Response(update, mimetype="application/json", status=200)


class UpdatesAPI(Resource):
    def get(self, plugin_name):
        updates = Plugin.objects.only('updates').get_or_404(name=plugin_name).to_json()
        return Response(updates, mimetype="application/json", status=200)

    def post(self, plugin_name):
        body = request.get_json()
        plugin = Plugin.objects.get(name=plugin_name)
        plugin.updates.append(PluginUpdate(**body))
        plugin.save()
        return '', 200


class TestAPI(Resource):
    def post(self,):
        SpigotPlugin(name="Thirst",
                     spigot_name="Thirst",
                     category="Mechanics",
                     average_rating="4.67",
                     upload_date=datetime.fromtimestamp(1465531920),
                     premium=False,
                     supported_versions=["1.9", "1.10", "1.11", "1.12"],
                     description="Adds an easy-to-use and highly configurable thirst mechanic right onto your server!",
                     resource_id=24610,
                     download_url="https://www.spigotmc.org/resources/thirst.24610/download?version=197410",
                     updates=[
                         PluginUpdate(server_id=uuid.uuid4(),
                                      timestamp=datetime.utcnow,
                                      size=335800,
                                      update_duration=0.18,
                                      version=PluginUpdateVersion(
                                          old="1.0.1-SNAPSHOT",
                                          new="1.0.1"))
                     ]).save()
