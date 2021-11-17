from celery import shared_task
from board.celery import app
from django.core.mail import EmailMessage
from board.settings import SEND_LOGS_TO


@app.task
def send_logs():
    message = EmailMessage(subject='logs',body='logs',from_email='grecigor11@gmail.com',to=SEND_LOGS_TO)
    message.attach_file('Forum/logs/info.log')
    if message.send():
        return "505"
    return '201'


