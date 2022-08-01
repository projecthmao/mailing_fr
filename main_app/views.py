import requests
import random
import os
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from dotenv import load_dotenv
from .models import Client, Mailing, Message
from .tasks import start_mailing as tasks_start_mailing
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """
        Summary data for a specific mailing list
        """
        queryset_mailing = Mailing.objects.all()
        get_object_or_404(queryset_mailing, pk=pk)
        queryset = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)    

    @action(detail=False, methods=['get'])
    def fullinfo(self, request):
        """
        Summary data for all mailings
        """
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Total number of mailings': total_count,
                'The number of messages lost': ''}
        result = {}
            
        for row in mailing:
            res = {'Total messages': 0, 'MAILED': 0, 'LOST': 0}
            mail = Message.objects.filter(mailing_id=row['id']).all()
            group_mailed = mail.filter(status='MAILED').count()
            group_lost = mail.filter(status='LOST').count()
            res['Total messages'] = len(mail)
            res['MAILED'] = group_mailed
            res['LOST'] = group_lost
            result[row['id']] = res
            
        content['The number of messages sent'] = result
        return Response(content)            
        
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


# сделаем случайный образом клиентов в тестовой базе
def create_clients(request):
    tags = ['sport','family','hobby','vacation',]
    Client.objects.all().delete()
    code_list=[922, 958, 919, 927, 950]
    for y in range(40):
        c = Client()

        code = code_list[random.randint(0,len(code_list)-1)]
        number = 7_000_000_0000 + code * 1_000_00_00 + random.randint(1,9) * 1_00_00_00 +random.randint(0,999999)
        c.mobile_number = number
        c.mobile_code = code
        c.time_zone = random.randint(-4,5)
        c.tag = tags[random.randint(0,len(tags)-1)]
        c.save()
    return HttpResponse('Hello,words')

# запуск отладки через браузер
def start_mailing(request):


    load_dotenv()
    url = os.getenv("URL")
    token = os.getenv("TOKEN")

    print(url)
    print(token)

    header = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    # requests.post(url=url + str(data['id']), headers=header, json=data)

    data = {
                'id': 110,
                "phone": 79222554059,
                "text": 'hello,world'
            }

    ans = requests.post(url=url + str(110), headers=header, json=data)
    if ans.reason == 'OK':
        print('ok, ok, ok!!!')
    


    # tasks_start_mailing()
    return HttpResponse('stared mailing')
