
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .organisation import Organisation

class Entity(models.Model):
    """
    This represents an 'user' of the platform, being automated or not
    """

    HUMAN = "HUMAN"
    ROBOT = "ROBOT"

    TYPE_CHOICES = (
        (HUMAN, HUMAN),
        (ROBOT, ROBOT),
    )

    org = models.ForeignKey(Organisation)
    name = models.TextField()
    entity_type = models.TextField(choices=TYPE_CHOICES)

    user = models.ForeignKey(User, blank=True, null=True) # FIXME: if type == Human, this must be set.

    def __str__(self):
        return "Entity { %s, %s, %s }" % (self.name, self.org, self.entity_type)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    """
    Administrator class for Entity.
    """
    list_display = ('user', 'org', 'entity_type')
