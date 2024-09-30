from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import All_knifes, Account_table



class All_knifesResource(resources.ModelResource):
    class Meta:
        model = All_knifes


class Account_tableResource(resources.ModelResource):
    class Meta:
        model = Account_table


@admin.register(All_knifes)
class All_knifesAdmin(ImportExportModelAdmin):
    resource_class = All_knifesResource
    list_display = ['brand', 'series', 'steel', 'carbon', 'CrMoV', 'angle', 'honing_add', 'category']


@admin.register(Account_table)
class Account_tableAdmin(ImportExportModelAdmin):
    resource_class = Account_tableResource
    list_display = ['date', 'brand', 'series', 'steel', 'carbon', 'CrMoV', 'length', 'width', 'grinding_angle',
                    'honing_add', 'comments', 'user']

