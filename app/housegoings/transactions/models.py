import csv
import decimal
import logging

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from housegoings.banks.models import BankAccount
from housegoings.core.helpers import normalize_string
from housegoings.core.models import HistoryModel, Currency

logger = logging.getLogger('django')


class Transaction(HistoryModel):
    class Types(models.TextChoices):
        INCOME = 'in', _('Income')
        EXPENSE = 'ex', _('Expense')

    transaction_date = models.DateField()
    type = models.CharField(max_length=2, choices=Types.choices, blank=False, null=False)
    value = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False)
    description = models.CharField(max_length=512, null=True, blank=True)
    bank_account = models.ForeignKey('banks.BankAccount', null=False, blank=False, on_delete=models.CASCADE)
    currency = models.ForeignKey('core.Currency', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'{self.transaction_date} {self.value}'

    def clean(self):
        super().clean()
        if self.value < 0 and self.type == Transaction.Types.INCOME:
            raise ValidationError(_('Income have to be greater than zero.'))
        if self.value > 0 and self.type == Transaction.Types.EXPENSE:
            raise ValidationError(_('Expense have to be lower than zero.'))

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.bank_account.funds += self.value
            self.bank_account.save()
        else:
            old_value = Transaction.objects.get(pk=self.pk).value
            self.bank_account.funds += (old_value * -1)
            self.bank_account.funds += self.value
            self.bank_account.save()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.bank_account.funds -= self.value
        self.bank_account.save()
        super().delete(using, keep_parents)


class TransactionImport(HistoryModel):
    file = models.FileField(upload_to='transactions_csv')
    bank_account = models.ForeignKey('banks.BankAccount', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.bank_account.__str__()} - {self.file}'

    @transaction.atomic
    def import_data(self):
        config = self.bank_account.bank.configuration.config
        with open(self.file.path, newline=config.get('newline')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=config.get('delimiter'))
            for idx, row in enumerate(csv_reader):
                if idx >= config.get('start_row'):
                    fields = config.get('fields')
                    transaction_type = ('in' if row[fields['income']]
                                                and decimal.Decimal(row[fields['income']]) > 0 else 'ex')
                    value = (decimal.Decimal(row[fields['income']])
                             if row[fields['income']] else decimal.Decimal(row[fields['expense']]))
                    description = normalize_string(row[fields['description']])
                    try:
                        currency_name = row[fields['currency']]
                        currency = Currency.objects.get(name=currency_name)
                    except ObjectDoesNotExist:
                        raise ValidationError(_(f'Cannot find currency {currency_name}.'))
                    transaction_date = row[fields['transaction_date']]
                    Transaction.objects.create(bank_account=self.bank_account, type=transaction_type, value=value,
                                               description=description, currency=currency,
                                               transaction_date=transaction_date)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.import_data()
