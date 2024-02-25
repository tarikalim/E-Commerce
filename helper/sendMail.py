from flask_mail import Message
from creates_app import mail


def send_email(to, subject, body):
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)
