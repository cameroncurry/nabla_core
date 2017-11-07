#
# Copyright Cameron Curry (c) 2017
#


import uuid

from django.db.models import Model
from django.db.models import UUIDField
from django.db.models import DateTimeField


class UUIDModel(Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
