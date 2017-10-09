from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .organisation import Organisation

class Server(models.Model):
    """
    This represents an organisations server
    """
    org = models.ForeignKey(Organisation)
    public_id = models.TextField()
    name = models.TextField()

    host_name = models.TextField()

    last_ip = models.TextField()

    last_booted = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return "Server { %s, %s, %s }" % (self.name, self.org, self.public_id)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    """
    Administrator class for server.
    """
    list_display = ('name', 'org', 'public_id')
