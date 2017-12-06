#
# Copyright Cameron Curry (c) 2017
#

from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import FloatField
from django.db.models import CASCADE

from .uuid_model import UUIDModel


class QTBalance(UUIDModel):
    """
    Model containing Questrade Balance information.
    See http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-balances

    Attributes:
        qt_account (QTAccount): QTAccount associated to this balance.
        type (str): Questrade Balance type (PER_CURRENCY, COMBINED).
        currency (str): Currency of this balance (CAD, USD).
        cash (float): The amount of cash.
        market_value (float): The market value of this balance.
        total_equity (float): The total equity of this balance.
        buying_power (float): The buying power of this balance.
    """

    qt_account = ForeignKey('QTAccount', on_delete=CASCADE)
    type = CharField(max_length=64)
    currency = CharField(max_length=3)
    cash = FloatField()
    market_value = FloatField()
    total_equity = FloatField()
    buying_power = FloatField()
