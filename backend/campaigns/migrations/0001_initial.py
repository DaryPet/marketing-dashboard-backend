# Generated by Django 5.1.4 on 2025-01-11 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('spent_budget', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('channels', models.ManyToManyField(to='campaigns.channel')),
            ],
        ),
    ]
