# Generated by Django 4.0.5 on 2022-07-13 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_mailing_mobile_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='mobile_code',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
