# Generated by Django 4.0.1 on 2022-01-10 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0005_banktransactionimportconfig'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='transactions_csv')),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banks.bankaccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
