#
# Copyright Cameron Curry (c) 2017
#

from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import FloatField
from django.db.models import IntegerField
from django.db.models import TextField


from .uuid_model import UUIDModel


class QTActivity(UUIDModel):
    """
    Model containing Questrade Activity information.
    See http://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-activities

    Attributes:
        trade_date (datetime): Date the trade occurred
        transaction_date (datetime): Date the transaction occurred
        settlement_date (datetime): Date trade was settled
        action (str): Activity action eg. BUY, SELL
        symbol (str): Symbol of the involved instrument eg. AAPL
        symbol_id (int): Questrade id of the instrument
        description (str): Questrade description of the activity
        currency (str): Currency of the activity
        quantity (int): The quantity of the activity
        price (float): The price of the instrument
        gross_amount (float): Gross amount of the activity
        commission (float): Commission paid to Questrade
        net_amount (float): Net ammount of the activity
        type (str): The type of the Activity eg. Interest
    """

    trade_date = DateTimeField()
    transaction_date = DateTimeField()
    settlement_date = DateTimeField()
    action = CharField(max_length=64)
    symbol = CharField(max_length=64)
    symbol_id = IntegerField()
    description = TextField()
    currency = CharField(max_length=64)
    quantity = IntegerField()
    price = FloatField()
    gross_amount = FloatField()
    commission = FloatField()
    net_amount = FloatField()
    type = CharField(max_length=64)

    def __str__(self):
        return "QTActivity[{}]".format(self.description)
