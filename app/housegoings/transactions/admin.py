from django.contrib import admin

from housegoings.core.admin import HistoryAdmin, SuperUserAdmin
from housegoings.transactions.models import Transaction, TransactionImport


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('value', 'transaction_date', 'description', 'bank_account', 'currency', 'type')
    fields = (('type', 'value', 'currency',),
              ('transaction_date', 'bank_account',),
              ('description',)
              )
    autocomplete_fields = ('bank_account', 'currency',)
    list_filter = (('bank_account', admin.RelatedOnlyFieldListFilter), 'type', 'currency',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(bank_account__owner=request.user)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(TransactionImport)
class TransactionImportAdmin(HistoryAdmin, SuperUserAdmin):
    list_display = ('bank_account', 'file', 'created')
    fields = (('bank_account',),
              ('file',),
              ('created', 'modified',))

    autocomplete_fields = ('bank_account',)
    list_filter = (('bank_account', admin.RelatedOnlyFieldListFilter),)

    def get_queryset(self, request):
        return super(TransactionImportAdmin, self).get_queryset(request).filter(bank_account__owner=request.user)

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True