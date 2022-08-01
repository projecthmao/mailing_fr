from django.db import models

class Client(models.Model):
    time_zone = models.IntegerField()
    mobile_number = models.IntegerField()
    mobile_code = models.IntegerField(default=0)
    tag = models.CharField(max_length=255, default='')

    def __str__(self):
        return f'{self.mobile_number} | {self.mobile_code} | {self.time_zone} | {self.tag}'



class Mailing(models.Model):
    start_dt = models.DateTimeField()
    finish_dt = models.DateTimeField()
    text = models.CharField(max_length=255, default='')
    tag = models.CharField(max_length=255, default='', blank=True)
    mobile_code = models.IntegerField(blank=True)

    def __str__(self):
        return  f'{self.start_dt} | {self.finish_dt} | {self.text} | {self.tag} | {self.mobile_code}'



class Message(models.Model):
    mailing_dt = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=[('MAILED', 'Успешно'),('LOST','Потеряно'),], blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    @classmethod
    def id_to_send(cls, m, c):
        messages =  cls.objects.filter(mailing=m, client=c)
        if len(messages) == 0:
            message = Message(mailing=m, client=c)
            message.save()
        else:
            message = messages.first()
        
        if message.status == 'MAILED':
            return None
        else:
            return message.id
