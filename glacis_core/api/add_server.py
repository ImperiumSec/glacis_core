import logging
from ..models import EntityOnServer, AccessToken, Organisation, Server, Key, KeyFetchEvent, AuditNote, AuditEvent

logger = logging.getLogger('core.apis.get_keys')
from uuid import uuid4
from datetime import datetime

def addserver(request):
    """
    Add server API
    """

    # Input is something similar to:
    # {
    #
    #   "access_token": {
    #       "id": "uuid of token_id",
    #       "value": "token_value"
    #   },
    #   "hostname": { }
    # }

    # 1: decide if acceptable request
    data = request.validated_data

    token = AccessToken.get_validated_token(data["access_token"]["id"], data["access_token"]["value"])

    new_server = Server()
    new_server.org = token.org
    new_server.public_id = str(uuid4())
    new_server.name = data["hostname"]
    new_server.host_name = data["hostname"]

    new_server.last_ip = "Unknown"
    new_server.active = True

    new_server.save()

    reply = {
        "status": "ok",

        "id": new_server.public_id
    }

    return reply
