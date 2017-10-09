from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from uuid import uuid4

import bcrypt

from datetime import datetime
from .organisation import Organisation
from .entity import Entity


class AccessToken(models.Model):
    """
    This represents a token used by a user.
    """

    BCRYPT = "BCRYPT"

    TRAPDOOR_CHOICES = (
        (BCRYPT, BCRYPT),
    )

    org = models.ForeignKey(Organisation)

    public_id = models.TextField() # a uuid

    name = models.TextField(blank=True, null=True)
    trapdoor_value = models.TextField()
    trapdoor_mechanism = models.TextField(choices=TRAPDOOR_CHOICES)
    trapdoor_data = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField()
    created_by = models.ForeignKey(Entity)

    @staticmethod
    def generate_token(name, org, created_by, trapdoor_mechanism=BCRYPT):
        """
        Generates a random token *and saves it* and returns a tuple of public_id, token_value, model ref)
        """

        # 1. pick a random value
        token = str(uuid4())
        binary_tok = token.encode("ascii")

        new_tok = AccessToken()
        new_tok.name = name

        new_tok.created_by = created_by
        new_tok.created_on = datetime.now()

        # 2. using the trapdoor_mechanism

        if trapdoor_mechanism == AccessToken.BCRYPT:
            # Hash for the first time, with a randomly-generated salt
            new_tok.trapdoor_value = bcrypt.hashpw(binary_tok, bcrypt.gensalt())
            new_tok.trapdoor_mechanism = AccessToken.BCRYPT
            new_tok.trapdoor_data = "" # no value needed here

        else:
            raise Exception("The trapdoor mechanism %s was not a valid choice" % trapdoor_mechanism)

        new_tok.public_id = str(uuid4())
        new_tok.org = org

        new_tok.save()

        return new_tok.public_id, token, new_tok


    @staticmethod
    def get_validated_token(public_id, token_value):
        """
        Get a validated token given a token id and plain value
        """

        tok = AccessToken.objects.get(public_id = public_id)
        b_str = token_value.encode("ascii")

        # Check that a unhashed password matches one that has previously been
        if tok.trapdoor_mechanism == AccessToken.BCRYPT:
            if bcrypt.hashpw(b_str, tok.trapdoor_value.encode("ascii")) == tok.trapdoor_value.encode("ascii"):
                return tok
            else:
                raise Exception("Access token did not validate")
        else:
            raise Exception("The Data in the db was an invalid mechanism (%s)" % tok.trapdoor_mechanism)

    def __str__(self):
        return "AccessToken { %s, %s, %s, %s }" % (self.org, self.public_id, self.name, self.trapdoor_mechanism)


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    """
    Administrator class for AccessToken.
    """
    list_display = ('org', 'name', 'trapdoor_mechanism', 'public_id')
