import requests
import os
import datetime
from dotenv import load_dotenv
from time import sleep
from mailing.celery import app
from django.db.models import Q
from .models import Mailing, Message, Client


@app.task
def start_mailing():
    dt_now = datetime.datetime.now()
    mailings = Mailing.objects.filter( Q(start_dt__lte=dt_now) & Q(finish_dt__gte=dt_now) )
    for m in mailings:
        if m.mobile_code !=0:
            clients = Client.objects.filter(mobile_code=m.mobile_code)
        else:
            clients = Client.objects.all()
        if m.tag.strip():
            clients = clients.filter(tag=m.tag)
        for c in clients:
            id_to_send = Message.id_to_send(m, c)
            print(id_to_send)
            if id_to_send:
                send_message.apply_async((id_to_send,), )

@app.task
def send_message(id_to_send):
    load_dotenv()
    url = os.getenv("URL")
    token = os.getenv("TOKEN")

    print(url)
    print(token)
    

    header = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    # requests.post(url=url + str(data['id']), headers=header, json=data)

    message = Message.objects.get(pk=id_to_send)
    data = {
                'id': message.id,
                "phone": message.client.mobile_number,
                "text": message.mailing.text
            }

    ans = requests.post(url=url + str(message.id), headers=header, json=data)
    if ans.reason == 'OK':
        message.mailing_dt = datetime.datetime.now()
        message.status = 'MAILED'
        message.save()
    else:
        message.mailing_dt = datetime.datetime.now()
        message.status = 'LOST'
        message.save()

    

