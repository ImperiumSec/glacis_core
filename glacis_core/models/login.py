
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .server import Server
from .entity import Entity
from .key import Key


class Login(models.Model):
    """
    This represents an 'login' on a random computer
    """

    server = models.ForeignKey(Server)
    time = models.DateTimeField()

    key = models.ForeignKey(Key, blank=True, null=True)
    entity = models.ForeignKey(Entity)

    auth_success = models.BoolenField()
    non_key_login = models.BoolenField()

    command = models.BooleanField()
    command_string = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Login { %s, %s, %s }" % (self.server, self.time, self.entity)


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    """
    Administrator class for Entity.
    """
    list_display = ('server', 'entity', 'time', 'command')
