import logging
from ..models import EntityOnServer, AccessToken, Organisation, Server, Key, KeyFetchEvent, AuditNote, AuditEvent

logger = logging.getLogger('core.apis.get_keys')
from uuid import uuid4
from datetime import datetime

def organisation_api(request):
    """
    Org API
    """

    # Input is something similar to:
    # {
    #
    #   "access_token": {
    #       "id": "uuid of token_id",
    #       "value": "token_value"
    #   },
    #
    # }

    # 1: decide if acceptable request
    data = request.validated_data

    token = AccessToken.get_validated_token(data["access_token"]["id"], data["access_token"]["value"])

    reply = {
        "status": "ok",
        "organisation": token.org.name,
        "id": token.org.public_id
    }

    return reply
