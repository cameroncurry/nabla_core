from django.contrib import admin

from ..models import QTAccess
from .qt_access_admin import QTAccessAdmin


admin.site.register(QTAccess, QTAccessAdmin)
