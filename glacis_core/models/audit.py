#
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .server import Server
from .key import Key
from .entity import Entity
from .serverUser import ServerUser


class AuditEvent(models.Model):
    """
    This represents an event on the server that is being audited.
    """

    TYPE_LOGIN = "LOGIN"
    TYPE_KEYFETCH = "KEYFETCH"

    TYPE_CHOICES = (
        (TYPE_LOGIN, TYPE_LOGIN),
        (TYPE_KEYFETCH, TYPE_KEYFETCH),
    )

    STATUS_OK = "OK"
    STATUS_QUERIED = "QUERIED"
    STATUS_WARNING = "WARNING"
    STATUS_OPEN = "OPEN"
    STATUS_DANGER = "DANGER"

    STATUS_CHOICES = (
        (STATUS_OK, STATUS_OK),
        (STATUS_QUERIED, STATUS_QUERIED),
        (STATUS_WARNING, STATUS_WARNING),
        (STATUS_OPEN, STATUS_OPEN),
        (STATUS_DANGER, STATUS_DANGER),
    )

    public_id = models.TextField()
    server = models.ForeignKey(Server)
    audit_type = models.TextField(choices=TYPE_CHOICES)

    audit_status = models.TextField(choices = STATUS_CHOICES)

    reported_at = models.DateTimeField()

    def get_child_type(self):
        if self.audit_type == AuditEvent.TYPE_LOGIN:
            return LoginEvent.objects.get(pk=self.pk)
        elif self.audit_type == AuditEvent.TYPE_KEYFETCH:
            return KeyFetchEvent.objects.get(pk=self.pk)
        else:
            raise Exception("Unknown event type '%s'" % self.audit_type)

    def __str__(self):
        return "AuditEvent { %s, %s, %s, %s}" % (self.public_id, self.server, self.audit_type, self.audit_status)


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    """
    Administrator class for AuditEvent.
    """
    list_display = ('server', 'reported_at', 'audit_type', 'public_id', 'audit_status',)


class KeyFetchEvent(AuditEvent):

    keys_loaded = models.ManyToManyField(Key)

    def __str__(self):
        return "KeyFetchEvent { %s, %s, %s }" % (self.public_id, self.server, self.audit_type)


@admin.register(KeyFetchEvent)
class KeyFetchEventAdmin(admin.ModelAdmin):
    """
    Administrator class for KeyFetchEvent.
    """
    # FIXME: which username on the server was it for?
    list_display = ('server', 'reported_at', 'public_id',)


class LoginEvent(AuditEvent):

    key_used = models.ForeignKey(Key)
    entity = models.ForeignKey(Entity)
    remote_ip = models.TextField()
    server_ip = models.TextField()
    server_username = models.ForeignKey(ServerUser)

    def __str__(self):
         return "Login Event { %s, %s, %s }" % (self.public_id, self.server, self.entity, self.audit_status)


@admin.register(LoginEvent)
class LoginEventAdmin(admin.ModelAdmin):
    """
    Administrator class for KeyFetchEvent.
    """
    list_display = ('server', 'reported_at', 'public_id', 'audit_status',)


class LoginAttempt(AuditEvent):

    username = models.TextField()
    key_fp = models.TextField()
    remote_ip = models.TextField()
    server_ip = models.TextField()


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """
    Administrator class for KeyFetchEvent.
    """
    list_display = ('server', 'reported_at', 'username', 'remote_ip',)


class AuditNote(models.Model):
    """
    A note attached to an Audit entry.
    """

    audit = models.ForeignKey(AuditEvent)
    message = models.TextField()
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(Entity, null=True, blank=True)
    public_id = models.TextField()

    def __str__(self):
        return "AuditNote { %s, %s, %s }" % (self.audit, self.created_by, self.public_id)


@admin.register(AuditNote)
class AuditNoteAdmin(admin.ModelAdmin):
    """
    Administrator class for KeyFetchEvent.
    """
    list_display = ('audit', 'created_by', 'created_at', 'public_id')
