from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .server import Server

class ServerUser(models.Model):
    """
    This represents an user account on a server
    """

    name = models.TextField()
    server = models.ForeignKey(Server)

    active = models.BooleanField(default=True)

    def __str__(self):
        return "Server User { %s@%s %s}" % (self.name, self.server, self.active)


@admin.register(ServerUser)
class ServerUserAdmin(admin.ModelAdmin):
    """
    Administrator class for server user
    """
    list_display = ('name', 'server', 'active')
