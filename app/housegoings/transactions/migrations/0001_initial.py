# Generated by Django 4.0.1 on 2022-01-09 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('banks', '0004_bankaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_date', models.DateField()),
                ('type', models.CharField(choices=[('in', 'Income'), ('ex', 'Expense')], max_length=2)),
                ('value', models.DecimalField(decimal_places=2, max_digits=11)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banks.bankaccount')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.currency')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
