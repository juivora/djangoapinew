# from models import User
from celery import shared_task
from django.core.mail import send_mail
from djangoapi import settings


@shared_task(bind=True)
def send_verification_mail_func(self, activation_link, user):
    mail_subject = "Hye from celery"
    message = "Please verify your account."+activation_link
    # to_email = user.email
    to_email = 'juivora1990@gmail.com'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return
