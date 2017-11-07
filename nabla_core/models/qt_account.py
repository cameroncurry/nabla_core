#
# Copyright Cameron Curry (c) 2017
#

from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import BooleanField

from .uuid_model import UUIDModel


class QTAccount(UUIDModel):
    """
    Model containing Questrade Account information.
    See http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts
    
    Attributes:
        type (str): Questrade Account Type
        number (int): Questrade Account Number
        status (str): Questrade Account Status
        primary (bool): True if the account is primary
        client_account_type (str): Questrade Client Account Type
    """

    type = CharField(max_length=64)
    number = IntegerField(unique=True, db_index=True)
    status = CharField(max_length=64)
    primary = BooleanField()
    client_account_type = CharField(max_length=64)

    def __str__(self):
        return "QTAccount[type={}, number={}]".format(self.type, self.number)
