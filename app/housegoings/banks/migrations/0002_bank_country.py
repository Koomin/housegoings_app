# Generated by Django 4.0.1 on 2022-01-09 16:20

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='country',
            field=django_countries.fields.CountryField(default='PL', max_length=2),
            preserve_default=False,
        ),
    ]
