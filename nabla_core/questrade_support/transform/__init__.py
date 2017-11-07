#
# Copyright Cameron Curry (c) 2017
#

from questrade.access import QTAccess as APIQTAccess
from questrade.account import QTAccount as APIQTAccount
from questrade.account import QTActivity as APIQTActivity

from ...models import QTAccess
from ...models import QTAccount
from ...models import QTActivity


def qt_access_core_to_api_transform(qt_access: QTAccess):
    """
    Transforms a nable_core QTAccess to questrade API QTAccess.
    
    :param qt_access: QTAccess to be transformed
    :return: APIQTAccess
    """
    return APIQTAccess(access_token=qt_access.access_token,
                       token_type=qt_access.token_type,
                       expires_in=qt_access.expires_in,
                       refresh_token=qt_access.refresh_token,
                       api_server=qt_access.api_server)


def qt_account_api_to_core_transform(qt_account: APIQTAccount):
    """
    Transforms a questrade API QTAccount to nabla_core QTAccount.
    
    :param qt_account: APIQTAccess to be transformed
    :return: QTAccount
    """
    return QTAccount(type=qt_account.account_type,
                     number=qt_account.number,
                     status=qt_account.status,
                     primary=qt_account.is_primary,
                     client_account_type=qt_account.client_account_type)


def qt_activity_api_to_core_transform(qt_activity: APIQTActivity):
    """
    Transforms a questrade API QTactivity to nabla_core QTActivity.
    
    :param qt_activity: APIQTActivity to be transformed 
    :return: QTActivity
    """
    return QTActivity(trade_date=qt_activity.trade_date,
                      transaction_date=qt_activity.transaction_date,
                      settlement_date=qt_activity.settlement_date,
                      action=qt_activity.action,
                      symbol=qt_activity.symbol,
                      symbol_id=qt_activity.symbol_id,
                      description=qt_activity.description,
                      currency=qt_activity.currency,
                      quantity=qt_activity.quantity,
                      price=qt_activity.price,
                      gross_amount=qt_activity.gross_amount,
                      commission=qt_activity.commission,
                      net_amount=qt_activity.net_amount,
                      type=qt_activity.activity_type)
