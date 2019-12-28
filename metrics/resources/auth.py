# metrics/resources/auth.py
"""Handled JWT authentication for the API."""
import datetime
import uuid

from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mongoengine import DoesNotExist

from metrics.database.models import MinecraftServer


class AuthAPI(Resource):
    """API for authenticating with JWT."""
    @staticmethod
    def post():
        """Register a minecraft server in exchange for a JWT token."""
        body = request.get_json()
        if body.get('ip') is not None:
            try:
                server = MinecraftServer.objects.get(ip=body.get('ip'))
            except DoesNotExist:
                server = MinecraftServer(**body)
                if not server.validate_server():
                    return {'error': 'Invalid Minecraft server.'}, 500
                server.id = uuid.uuid4()
        else:
            return {'error': 'No ip field provided.'}, 500

        server.save()
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(server.id), expires_delta=expires)
        return {'token': access_token}, 200
