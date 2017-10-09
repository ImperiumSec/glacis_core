from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Organisation(models.Model):
    """
    This represents an organisational entity.
    """
    owner = models.ForeignKey(User)
    public_id = models.TextField()
    name = models.TextField()


    def __str__(self):
        return "Org { %s, %s }" % (self.name, self.public_id)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """
    Administrator class for Org.
    """
    list_display = ('name', 'owner', 'public_id')
