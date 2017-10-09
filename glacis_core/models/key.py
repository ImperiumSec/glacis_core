from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .entity import Entity

class Key(models.Model):
    """
    This represents an users public key
    """

    owner = models.ForeignKey(Entity)
    key = models.TextField()
    public_id = models.TextField()
    name = models.TextField()

    default = models.BooleanField()

    active = models.BooleanField(default=True)

    # audit fields
    created_on = models.DateTimeField()
    key_fingerprint = models.TextField()
    key_type = models.TextField()
    key_length = models.IntegerField()


    def __str__(self):
        return "Key { %s, %s, %s }" % (self.owner.name, self.name, self.public_id)


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    """
    Administrator class for Key.
    """
    list_display = ('owner', 'name', 'public_id')
