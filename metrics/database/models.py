# metrics/database/models.py
import datetime

from .db import db


class PluginUpdateVersion(db.EmbeddedDocument):
    old = db.StringField(required=True)
    new = db.StringField(required=True)


class PluginUpdate(db.EmbeddedDocument):
    server_id = db.UUIDField(required=True)
    timestamp = db.DateTimeField(default=datetime.datetime.utcnow)
    size = db.IntField(required=True)
    update_duration = db.DecimalField(required=True)
    version = db.EmbeddedDocumentField(PluginUpdateVersion, required=True)


class Plugin(db.Document):
    name = db.StringField(required=True, primary_key=True)
    description = db.StringField()
    download_url = db.URLField()
    updates = db.EmbeddedDocumentListField(PluginUpdate)
    meta = {'allow_inheritance': True}

    # @staticmethod
    # def encode_auth_token(server_ip):
    #     try:
    #         payload = {
    #             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
    #             'iat': datetime.datetime.utcnow(),
    #             'sub': server_ip
    #         }
    #         return jwt.encode(
    #             payload,
    #             app.config.get('SECRET_KEY'),
    #             algorithm='HS256'
    #         )
    #     except Exception as e:
    #         return e


class SpigotPlugin(Plugin):
    spigot_name = db.StringField(required=True)
    resource_id = db.IntField(required=True)
    category = db.StringField(required=True)
    average_rating = db.DecimalField(required=True)
    upload_date = db.DateTimeField(required=True)
    supported_versions = db.ListField(db.StringField(), required=True)
    premium = db.BooleanField(required=True)
    price = db.DecimalField()
    currency = db.StringField()
