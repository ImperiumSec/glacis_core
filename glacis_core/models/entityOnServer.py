from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .server import Server
from .serverUser import ServerUser
from .entity import Entity
from .key import Key

class EntityOnServer(models.Model):
    """
    This represents the relationship between entity and server
    """

    server_user = models.ForeignKey(ServerUser) ### WIRTING HERE - REDRAWING GRAPH
    entity = models.ForeignKey(Entity)
    named_key = models.ForeignKey(Key, null=True, blank=True)

    def __str__(self):
        if self.named_key:
            return "Entity { %s, %s, %s }" % (self.server_user.name, self.entity.name, self.named_key.name)
        else:
            return "Entity { %s, %s, Default }" % (self.server_user.name, self.entity.name)


@admin.register(EntityOnServer)
class EntityOnServerAdmin(admin.ModelAdmin):
    """
    Administrator class for Entity on a server
    """
    list_display = ('server_user', 'entity', 'named_key')
