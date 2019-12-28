# metrics/database/models.py
"""Database models."""
import datetime
from _socket import gaierror, timeout

from .db import db
from ..utils.statusping import StatusPing


class MinecraftServer(db.Document):
    """Stores information about specific minecraft servers."""
    id = db.UUIDField(required=True, primary_key=True)
    ip = db.StringField()
    motd = db.StringField()

    def validate_server(self):
        """Validates that the server is a valid minecraft server."""
        if self.ip is not None:
            try:
                status = StatusPing(host=self.ip).get_status()
                self.motd = str(status['description'])
                return True
            except (gaierror, timeout):
                return False
        else:
            return False


class PluginUpdateVersion(db.EmbeddedDocument):
    """An embedded document for plugin update versions."""
    old = db.StringField(required=True)
    new = db.StringField(required=True)


class PluginUpdate(db.EmbeddedDocument):
    """An embedded document for updates of plugins."""
    server_id = db.UUIDField(required=True)
    timestamp = db.DateTimeField(default=datetime.datetime.utcnow)
    size = db.IntField(required=True)
    update_duration = db.DecimalField(required=True)
    version = db.EmbeddedDocumentField(PluginUpdateVersion, required=True)


class Plugin(db.Document):
    """Base document for plugins."""
    name = db.StringField(required=True, primary_key=True)
    description = db.StringField()
    download_url = db.URLField()
    updates = db.EmbeddedDocumentListField(PluginUpdate)
    meta = {'allow_inheritance': True}


class SpigotPlugin(Plugin):
    """An extended document specifically for Spigot plugins."""
    spigot_name = db.StringField(required=True)
    resource_id = db.IntField(required=True)
    category = db.StringField(required=True)
    average_rating = db.DecimalField(required=True)
    upload_date = db.DateTimeField(required=True)
    supported_versions = db.ListField(db.StringField(), required=True)
    premium = db.BooleanField(required=True)
    price = db.DecimalField()
    currency = db.StringField()
