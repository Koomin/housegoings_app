from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class HistoryModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save_and_update(self, *args, **kwargs):
        for key, value in kwargs.items():
            try:
                self._meta.get_field(key)
            except FieldDoesNotExist:
                continue
            setattr(self, key, value)
        self.save()


class Currency(HistoryModel):
    name = models.CharField(max_length=3, null=False, blank=False)
    country = CountryField()

    class Meta:
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.name
