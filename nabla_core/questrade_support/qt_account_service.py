#
# Copyright Cameron Curry (c) 2017
#
import time
from datetime import datetime, timedelta
from questrade.account import QTAccountService as APIQTAccountService

from ..models import QTAccess
from ..models import QTAccount
from ..models import QTActivity
from .transform import qt_access_core_to_api_transform
from .transform import qt_account_api_to_core_transform
from .transform import qt_activity_api_to_core_transform


class QTAccountService:

    def __init__(self, qt_access: QTAccess):
        assert qt_access.scope == QTAccess.account_data_scope_entry(), 'QTAccess not in Account data scope'
        api_qt_access = qt_access_core_to_api_transform(qt_access)
        self._account_service = APIQTAccountService(api_qt_access)

    def accounts(self):
        """
        Retrieve all QTAccounts from Questrade.
        
        :return: QTAccount 
        """
        api_accounts = self._account_service.accounts()
        return [qt_account_api_to_core_transform(api_account) for api_account in api_accounts]

    def activities(self, qt_account: QTAccount, start, end):
        """
        Retrieve all QTActivities from Questrade.

        :return: QTActivity 
        """
        api_activities = self._account_service.activities(qt_account.number, start, end)
        return [qt_activity_api_to_core_transform(api_activity) for api_activity in api_activities]

    def sync_accounts(self):
        """
        Upsert all Questrade Accounts.
        
        :return: None
        """
        qt_accounts = self.accounts()
        for qt_account in qt_accounts:
            QTAccount.objects.update_or_create(
                number=qt_account.number,
                defaults={
                    'type': qt_account.type,
                    'status': qt_account.status,
                    'primary': qt_account.primary,
                    'client_account_type': qt_account.client_account_type
                }
            )

    def sync_activities(self, since=datetime(2014, 1, 1), until=datetime.today()):
        """
        Upsert all Questrade Activities from existing QTAccounts.
        
        :param since: Collect activities since this date.
        :param until: Until this date.
        :return: None
        """
        qt_accounts = QTAccount.objects.all()
        print(qt_accounts)
        for qt_account in qt_accounts:
            self._upsert_activities(qt_account, since, until)

    def _upsert_activities(self, qt_account, since, until):
        """
        Upsert all Questrade Activities for given QTAccount.
        
        :param qt_account: Activities for this QTAccount. 
        :param since: Collect activities since this date.
        :param until: Until this date.
        :return: None
        """

        questrade_timedelta_max = timedelta(days=30)

        i = 0
        while True:
            i += 1
            next_date = min(since + questrade_timedelta_max, until)
            # TODO implement better rate limting solution
            if i % 10 == 0:
                time.sleep(1)

            qt_activities = self.activities(qt_account, since, next_date)
            for qt_activity in qt_activities:
                QTActivity.objects.update_or_create(
                    trade_date=qt_activity.trade_date,
                    transaction_date=qt_activity.transaction_date,
                    settlement_date=qt_activity.settlement_date,
                    action=qt_activity.action,
                    symbol=qt_activity.symbol,
                    symbol_id=qt_activity.symbol_id,
                    currency=qt_activity.currency,
                    quantity=qt_activity.quantity,
                    price=qt_activity.price,
                    gross_amount=qt_activity.gross_amount,
                    commission=qt_activity.commission,
                    net_amount=qt_activity.net_amount,
                    type=qt_activity.type,
                    defaults={'description': qt_activity.description}
                )

            since = next_date
            if next_date >= until:
                break

