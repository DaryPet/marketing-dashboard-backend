# Generated by Django 5.1.4 on 2025-01-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(choices=[('TV', 'Television'), ('Social Media', 'Social Networks'), ('Radio', 'Radio'), ('Search Engine', 'Search Engines')], max_length=50),
        ),
        migrations.AlterField(
            model_name='channel',
            name='type',
            field=models.CharField(choices=[('TV', 'Television'), ('Social Media', 'Social Networks'), ('Radio', 'Radio'), ('Search Engine', 'Search Engines')], max_length=50),
        ),
    ]
