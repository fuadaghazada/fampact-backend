from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _('FamPact Administration')
admin.site.site_url = None
admin.site.enable_nav_sidebar = False
