# Generated by Django 4.0.5 on 2022-07-21 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_message_mailing_dt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='mobile_code',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Delivery_Service',
        ),
    ]