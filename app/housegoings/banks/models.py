from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from localflavor.generic.models import IBANField

from housegoings.core.models import HistoryModel


class Bank(HistoryModel):
    name = models.CharField(blank=False, null=False, max_length=120)
    country = CountryField()

    def __str__(self):
        return self.name


class BankAccount(HistoryModel):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=False, related_name='bank_accounts')
    account_number = IBANField()
    funds = models.DecimalField(default=Decimal(0.00), max_digits=16, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='bank_accounts')

    def __str__(self):
        return f'{self.bank.name} - {self.account_number}'


class BankTransactionImportConfig(HistoryModel):
    bank = models.OneToOneField(Bank, on_delete=models.CASCADE, null=False, related_name='configuration')
    config = models.JSONField(default=dict)

    def __str__(self):
        return f'Config - {self.bank.__str__()}'
