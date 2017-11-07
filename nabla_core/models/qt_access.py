#
# Copyright Cameron Curry (c) 2017
#

from django.db.models import URLField
from django.db.models import CharField
from django.db.models import IntegerField

from .uuid_model import UUIDModel


class QTAccess(UUIDModel):
    """
    Model containing questrade api access information.
    See http://www.questrade.com/api/documentation/security
    
    Attributes:
        scope (str): Scope of the Access token either Account data, Market data, or Order placement
        access_token (str): Access token for making authenticated calls.
        token_type (str): Type of token (always set to “Bearer”).
        expires_in (int): Duration of the time token in which it became active (in seconds).
        refresh_token (str): Refresh token received from the security centre.
        api_server (str): URL of the API server that the client application should contact.
    """

    SCOPE_CHOICES = (
        ('ACC', 'Account data'),
        ('MKT', 'Market data'),
        ('ODR', 'Order placement'),
    )

    scope = CharField(max_length=3, choices=SCOPE_CHOICES)
    access_token = CharField(max_length=64)
    token_type = CharField(max_length=64)
    expires_in = IntegerField(default=0)
    refresh_token = CharField(max_length=64)
    api_server = URLField(max_length=64)

    def __str__(self):
        return "QTAccess[scope={}, refresh_token={}, access_token={}".format(self.scope,
                                                                             self.refresh_token,
                                                                             self.access_token)

    @staticmethod
    def account_data_scope_entry():
        return QTAccess.SCOPE_CHOICES[0][0]

    @staticmethod
    def market_data_scope_entry():
        return QTAccess.SCOPE_CHOICES[1][0]

    @staticmethod
    def order_placement_scope_entry():
        return QTAccess.SCOPE_CHOICES[2][0]
