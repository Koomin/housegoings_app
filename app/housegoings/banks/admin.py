from django.contrib import admin

from housegoings.banks.models import Bank, BankAccount, BankTransactionImportConfig
from housegoings.core.admin import SuperUserAdmin


class BankImportConfigInline(admin.StackedInline):
    model = BankTransactionImportConfig


@admin.register(Bank)
class BankAdmin(SuperUserAdmin):
    list_display = ('name', 'country')
    fields = (('name', 'country'),
              ('created', 'modified'))
    search_fields = ('name',)
    list_filter = ('country',)
    inlines = [BankImportConfigInline]

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'bank', 'funds')
    fields = (('account_number', 'bank'),
              ('funds',))
    autocomplete_fields = ('bank',)
    search_fields = ('account_number', 'bank',)
    list_filter = ('bank__name',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields = list(readonly_fields)
            readonly_fields.append('funds')
            readonly_fields = tuple(readonly_fields)
        return readonly_fields
