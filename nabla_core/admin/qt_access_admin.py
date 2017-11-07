#
# Copyright Cameron Curry (c) 2017
#

from django.contrib.admin import ModelAdmin

from ..questrade_support import QTAccessService


class QTAccessAdmin(ModelAdmin):

    fields = ['scope', 'refresh_token']
    list_display = ('scope', 'refresh_token', 'modified')
    list_filter = ['scope']
    actions = ['refresh']

    def refresh(self, request, queryset):
        for qt_access in queryset:
            QTAccessService.refresh_and_save_qt_access(qt_access)
        self.message_user(request, 'Successfully refreshed QTAccesses.')

    refresh.short_description = 'Refresh selected tokens'
