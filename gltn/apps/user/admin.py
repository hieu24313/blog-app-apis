from django.contrib import admin
from .models import CustomUser
# Register your models here.


class ThesisAppAdminSite(admin.AdminSite):
    site_header = 'Giao Lưu Tennis'


admin_site = ThesisAppAdminSite(name='Giao Lưu Tennis')


admin_site.register(CustomUser)
