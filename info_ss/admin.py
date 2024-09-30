from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Info_table

# Register your models here.
class Info_tableResource(resources.ModelResource):
    class Meta:
        model = Info_table


@admin.register(Info_table)
class Info_tableAdmin(ImportExportModelAdmin):
    resource_class = Info_tableResource
    list_display = [
        'date_of_visit',
        'visitor_id',
        'visitor_name',
        'visitor_IP',
        'visitor_email',
        'visitor_tz',
        'choose_visits',
        'calculation_visits',
        'account_table_visits'
    ]