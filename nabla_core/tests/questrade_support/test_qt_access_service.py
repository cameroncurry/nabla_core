#
# Copyright Cameron Curry (c) 2017
#

from unittest.mock import patch
from django.test import TestCase

from nabla_core.models import QTAccess
from nabla_core.questrade_support import QTAccessService


class TestQTAccessService(TestCase):

    def setUp(self):
        self.created_qt_access = QTAccess.objects.create(scope=QTAccess.account_data_scope_entry(),
                                                         refresh_token='aSBe7wAAdx88QTbwut0tiu3SYic3ox8F')

    @patch('questrade.access.QTAccessService.refresh')
    def test_refresh_and_save(self, mock):
        mock.return_value.access_token = 'C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp'
        mock.return_value.token_type = 'Bearer'
        mock.return_value.expires_in = 300
        mock.return_value.refresh_token = 'aSBe7wAAdx88QTbwut0tiu3SYic3ox8F'
        mock.return_value.api_server = 'https://api01.iq.questrade.com'

        qt_access = QTAccess.objects.get(scope='ACC')

        saved_qt_access = QTAccessService.refresh_and_save_qt_access(qt_access)
        refreshed_qt_access = QTAccess.objects.get(scope='ACC')
        expected_access = (
            (saved_qt_access.id, self.created_qt_access.id),
            (saved_qt_access.access_token, 'C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp'),
            (saved_qt_access.token_type, 'Bearer'),
            (saved_qt_access.expires_in, 300),
            (saved_qt_access.refresh_token, 'aSBe7wAAdx88QTbwut0tiu3SYic3ox8F'),
            (saved_qt_access.api_server, 'https://api01.iq.questrade.com'),
            (refreshed_qt_access.id, self.created_qt_access.id),
            (refreshed_qt_access.access_token, 'C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp'),
            (refreshed_qt_access.token_type, 'Bearer'),
            (refreshed_qt_access.expires_in, 300),
            (refreshed_qt_access.refresh_token, 'aSBe7wAAdx88QTbwut0tiu3SYic3ox8F'),
            (refreshed_qt_access.api_server, 'https://api01.iq.questrade.com')
        )
        for result, expected in expected_access:
            with self.subTest(result=result):
                self.assertEqual(result, expected)
