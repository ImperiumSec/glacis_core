from ..models import EntityOnServer, AccessToken, Organisation, Server, ServerUser, Key, KeyFetchEvent, AuditNote, AuditEvent, LoginAttempt
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from uuid import uuid4
from datetime import datetime

import json

@csrf_exempt
def get_keys(request):
    """
    Get Keys API - used in conjunction with the v2.1 client
    """

    # input is something similar to:

    # {
    #   "server_id":
    #   "access_token": {
    #      id:""
    #      value:""
    #   },
    #   username: ""
    #   origin_ip: ""
    #   key_fp: ""
    #   key_type: ""
    # }

    data = json.loads(request.body)

    # 1. Decide if acceptable request
    token = AccessToken.get_validated_token(data["access_token"]["id"], data["access_token"]["value"])

    # Validate access_token

    # FIXME: refaactor all this code to prevent data leakage through errors

    server = Server.objects.filter(active=True).filter(org=token.org).filter(public_id=data["server_id"]).get()

    la = LoginAttempt()
    la.username = data['username']
    la.key_fp = data['key_fp']
    la.remote_ip = data['origin_ip']
    la.server_ip = request.META['REMOTE_ADDR']

    la.public_id = str(uuid4())
    la.server = server
    la.audit_type = AuditEvent.TYPE_KEYFETCH
    la.audit_status = AuditEvent.STATUS_OPEN
    la.reported_at = datetime.now()

    la.save()
    
    # 2. pull key data
    key = None

    server_user = ServerUser.objects.filter(server=server).filter(name=data["username"])

    target_key = Key.objects.filter(key_fingerprint=data["key_fp"]).get()

    cont = True

    if server_user == 0:
        # login attempt
        cont = False

    if target_key == 0:
        cont = False

    if cont:
        # look for EntityOnServer to match
        try:
            target_eos = EntityOnServer.objects.filter(server_user=server_user).filter(named_key=target_key).get()
            #print("EOS %s" % target_eos )
            key = target_key
        except Exception:
            # FIXME: do a nicer exception
            
            targets = EntityOnServer.objects.filter(server_user=server_user).filter(entity=target_key.owner)
            if len(targets) > 0:
                key = target_key
            else:
                raise Exception("Boom")

        else:
            key = Key.objects.filter(owner=target_eos.entity).filter(id=target_key.id).get()
        
        if key.active and key.key_fingerprint == data["key_fp"]:
            pass
        else:
            key = None
            
    # Key should now be a Key object
    #print ("--> %s" % key)
    output = ""
    if key:
        sub_template = Template("ssh-rsa {{ key.key }}")
   
        c = Context({"key":key})
        output = sub_template.render(c)

    return HttpResponse(output)