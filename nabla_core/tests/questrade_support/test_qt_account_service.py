#
# Copyright Cameron Curry (c) 2017
#

from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from django.test import TestCase

from questrade.account import QTAccount as APIQTAccount
from questrade.account import QTBalance as APIQTBalance
from questrade.account import QTActivity as APIQTActivity

from nabla_core.models import QTAccess
from nabla_core.models import QTAccount
from nabla_core.models import QTBalance
from nabla_core.models import QTActivity
from nabla_core.questrade_support import QTAccountService


class TestQTAccountService(TestCase):

    def setUp(self):
        qt_access = QTAccess(scope=QTAccess.account_data_scope_entry(),
                             access_token='C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp',
                             token_type='Bearer',
                             expires_in=300,
                             refresh_token='aSBe7wAAdx88QTbwut0tiu3SYic3ox8F',
                             api_server='https://api01.iq.questrade.com/')

        self.account_service = QTAccountService(qt_access)

    @patch('questrade.account.QTAccountService.accounts')
    def test_accounts(self, mock):
        mock.return_value = [
            APIQTAccount(account_type='Margin',
                         number=26598145,
                         status='Active',
                         is_primary=True,
                         is_billing=True,
                         client_account_type='Individual')
        ]

        qt_accounts = self.account_service.accounts()
        self.assertEqual(len(qt_accounts), 1)
        self.assertIsInstance(qt_accounts[0], QTAccount)
        expected_accounts = (
            (qt_accounts[0].type, 'Margin'),
            (qt_accounts[0].number, 26598145),
            (qt_accounts[0].status, 'Active'),
            (qt_accounts[0].primary, True),
            (qt_accounts[0].client_account_type, 'Individual')
        )
        for result, expected in expected_accounts:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    @patch('questrade.account.QTAccountService.balances')
    def test_balances(self, mock):
        mock.return_value = [
            APIQTBalance(balance_type=APIQTBalance.BalanceType.COMBINED,
                         currency='CAD',
                         cash=243971.7,
                         market_value=6017,
                         total_equity=249988.7,
                         buying_power=496367.2,
                         maintenance_excess=248183.6,
                         is_real_time=True),
            APIQTBalance(balance_type=APIQTBalance.BalanceType.COMBINED,
                         currency='USD',
                         cash=198259.05,
                         market_value=53745,
                         total_equity=252004.05,
                         buying_power=461013.3,
                         maintenance_excess=230506.65,
                         is_real_time=True)
        ]

        qt_account = QTAccount(type='Margin',
                               number=26598145,
                               status='Active',
                               primary=True,
                               client_account_type='Individual')

        qt_balances = self.account_service.balances(qt_account)
        self.assertEqual(len(qt_balances), 2)
        self.assertIsInstance(qt_balances[0], QTBalance)
        self.assertIsInstance(qt_balances[1], QTBalance)
        expected_balances = (
            (qt_balances[0].type, 'COMBINED'),
            (qt_balances[0].currency, 'CAD'),
            (qt_balances[0].cash, 243971.7),
            (qt_balances[0].market_value, 6017),
            (qt_balances[0].total_equity, 249988.7),
            (qt_balances[0].buying_power, 496367.2),
            (qt_balances[1].type, 'COMBINED'),
            (qt_balances[1].currency, 'USD'),
            (qt_balances[1].cash, 198259.05),
            (qt_balances[1].market_value, 53745),
            (qt_balances[1].total_equity, 252004.05),
            (qt_balances[1].buying_power, 461013.3),
        )
        for result, expected in expected_balances:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    @patch('questrade.account.QTAccountService.activities')
    def test_activities(self, mock):
        mock.return_value = [
            APIQTActivity(trade_date=datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5))),
                          transaction_date=datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5))),
                          settlement_date=datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5))),
                          action='',
                          symbol='',
                          symbol_id=0,
                          description='INT FR 02/04 THRU02/15@ 4 3/4%BAL  205,006   AVBAL  204,966 ',
                          currency='USD',
                          quantity=0,
                          price=0.0,
                          gross_amount=0.0,
                          commission=0.0,
                          net_amount=-320.08,
                          activity_type='Interest')
        ]

        qt_account = QTAccount(type='Margin',
                               number=26598145,
                               status='Active',
                               primary=True,
                               client_account_type='Individual')
        start = datetime(2011, 2, 1, tzinfo=timezone(timedelta(hours=-5)))
        end = datetime(2011, 2, 28, tzinfo=timezone(timedelta(hours=-5)))

        qt_activities = self.account_service.activities(qt_account, start, end)
        self.assertEqual(len(qt_activities), 1)
        self.assertIsInstance(qt_activities[0], QTActivity)
        expected_activities = (
            (qt_activities[0].trade_date, datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5)))),
            (qt_activities[0].transaction_date, datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5)))),
            (qt_activities[0].settlement_date, datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5)))),
            (qt_activities[0].action, ''),
            (qt_activities[0].symbol, ''),
            (qt_activities[0].symbol_id, 0),
            (qt_activities[0].description, 'INT FR 02/04 THRU02/15@ 4 3/4%BAL  205,006   AVBAL  204,966 '),
            (qt_activities[0].currency, 'USD'),
            (qt_activities[0].quantity, 0),
            (qt_activities[0].price, 0.0),
            (qt_activities[0].commission, 0.0),
            (qt_activities[0].net_amount, -320.08),
            (qt_activities[0].type, 'Interest')
        )
        for result, expected in expected_activities:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    @patch('questrade.account.QTAccountService.accounts')
    def test_sync_accounts(self, mock):
        mock.return_value = [
            APIQTAccount(account_type='Margin',
                         number=26598145,
                         status='Active',
                         is_primary=True,
                         is_billing=True,
                         client_account_type='Individual')
        ]
        self.account_service.sync_accounts()
        qt_account = QTAccount.objects.get(number=26598145)
        expected_accounts = (
            (qt_account.type, 'Margin'),
            (qt_account.number, 26598145),
            (qt_account.status, 'Active'),
            (qt_account.primary, True),
            (qt_account.client_account_type, 'Individual')
        )
        for result, expected in expected_accounts:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    @patch('questrade.account.QTAccountService.accounts')
    def test_sync_accounts_with_existing(self, mock):
        mock.return_value = [
            APIQTAccount(account_type='Margin',
                         number=26598145,
                         status='Active',
                         is_primary=True,
                         is_billing=True,
                         client_account_type='Individual'),
            APIQTAccount(account_type='Cash',
                         number=26598146,
                         status='Active',
                         is_primary=False,
                         is_billing=True,
                         client_account_type='Individual')
        ]

        QTAccount.objects.create(type='Margin',
                                 number=26598146,
                                 status='Active',
                                 primary=True,
                                 client_account_type='Individual')

        self.account_service.sync_accounts()
        qt_accounts = QTAccount.objects.all()
        expected_accounts = (
            (qt_accounts[0].type, 'Margin'),
            (qt_accounts[0].number, 26598145),
            (qt_accounts[0].status, 'Active'),
            (qt_accounts[0].primary, True),
            (qt_accounts[0].client_account_type, 'Individual'),
            (qt_accounts[1].type, 'Cash'),
            (qt_accounts[1].number, 26598146),
            (qt_accounts[1].status, 'Active'),
            (qt_accounts[1].primary, False),
            (qt_accounts[1].client_account_type, 'Individual')
        )
        for result, expected in expected_accounts:
            with self.subTest(result=result):
                self.assertEqual(result, expected)
