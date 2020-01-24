# metrics/database/models.py
"""Database models."""
import datetime
from _socket import gaierror, timeout

from metrics.resources.minecraft_status_checker import StatusPing
from .db import DB


class MinecraftServer(DB.Document):
    """Stores information about specific minecraft servers."""
    id = DB.UUIDField(required=True, primary_key=True)
    ip = DB.StringField()
    motd = DB.StringField()

    def validate_server(self):
        """Validates that the server is a valid minecraft server."""
        if self.ip is not None:
            try:
                status = StatusPing(host=self.ip).get_status()
                self.motd = str(status['description'])
                return True
            except (gaierror, timeout, ConnectionRefusedError):
                return False
        else:
            return False

    def update_server(self):
        """Updates information about the minecraft server, without inhibiting response time (if run async)."""
        try:
            status = StatusPing(host=self.ip).get_status()
            self.motd = str(status['description'])
            self.save()
        except (gaierror, timeout, ConnectionRefusedError):
            self.delete()


class PluginUpdateVersion(DB.EmbeddedDocument):
    """An embedded document for plugin update versions."""
    old = DB.StringField()
    new = DB.StringField(required=True)


class PluginUpdate(DB.EmbeddedDocument):
    """An embedded document for updates of plugins."""
    server_id = DB.UUIDField(required=True)
    timestamp = DB.DateTimeField(default=datetime.datetime.utcnow)
    cached = DB.BooleanField()
    replaced_old = DB.BooleanField()
    size = DB.IntField(required=True)
    update_duration = DB.DecimalField(required=True)
    version = DB.EmbeddedDocumentField(PluginUpdateVersion, required=True)


class Plugin(DB.Document):
    """Base document for plugins."""
    id = DB.UUIDField(required=True, primary_key=True)
    name = DB.StringField(required=True)
    description = DB.StringField()
    download_url = DB.URLField()
    updates = DB.EmbeddedDocumentListField(PluginUpdate)
    meta = {'allow_inheritance': True}


class SpigotPlugin(Plugin):
    """An extended document specifically for Spigot plugins."""
    spigot_name = DB.StringField(required=True)
    resource_id = DB.IntField(required=True)
    category = DB.StringField(required=True)
    average_rating = DB.DecimalField()
    upload_date = DB.DateTimeField(required=True)
    supported_versions = DB.ListField(DB.StringField())
    premium = DB.BooleanField()
    price = DB.DecimalField()
    currency = DB.StringField()
