from django.contrib import admin

from housegoings.core.models import Currency


class HistoryAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified',]


class SuperUserAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    fields = (('name',),
              ('country',))
    search_fields = ('name', 'country')
