# Generated by Django 4.2.2 on 2024-07-31 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dog',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
