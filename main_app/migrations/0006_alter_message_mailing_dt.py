# Generated by Django 4.0.5 on 2022-07-20 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_message_mailing_dt_alter_message_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='mailing_dt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
