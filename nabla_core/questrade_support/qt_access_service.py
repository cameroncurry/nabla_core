#
# Copyright Cameron Curry (c) 2017
#

from questrade.access import QTAccessService as APIQTAccessService

from nabla_core.models import QTAccess


class QTAccessService:

    @staticmethod
    def refresh_and_save_qt_access(qt_access: QTAccess):
        """
        Makes API call to questrade and updates the persistent QTAccess with new access token etc.
        
        :param qt_access: QTAccess object to be refreshed. 
        :return: None
        """
        api_qt_access = APIQTAccessService.refresh(qt_access.refresh_token)
        qt_access.access_token = api_qt_access.access_token
        qt_access.token_type = api_qt_access.token_type
        qt_access.expires_in = api_qt_access.expires_in
        qt_access.refresh_token = api_qt_access.refresh_token
        qt_access.api_server = api_qt_access.api_server
        qt_access.save()
        return qt_access
