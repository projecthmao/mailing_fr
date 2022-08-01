from mailbox import Mailbox
from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_zone', 'mobile_code', 'mobile_number', 'tag',)

class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_dt', 'finish_dt', 'text', 'tag', 'mobile_code',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_dt', 'status', 'client', 'mailing',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(Message, MessageAdmin)
