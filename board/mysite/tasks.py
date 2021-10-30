from celery import shared_task
from board.celery import app
from django.core.mail import EmailMessage
import os


@app.task
def send_logs():
    message = EmailMessage(subject='logs',body='logs',from_email='grecigor11@gmail.com',to=('grecigor25@gmail.com','lobashov_kirill@mail.ru'))
    message.attach_file('Forum/logs/info.log')
    message.send()
    return '201'


