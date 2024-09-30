from __future__ import absolute_import
from celery import shared_task
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@shared_task()
def send_email_for_varify_delay(message, email):
    email_delay = EmailMessage('Verify email', message, to=[email])
    email_delay.send()


# формирование и отправление на email ссылки для подтверждения регистрации с новым email
def send_email_for_varify(request, user, new_email):
    current_site = get_current_site(request)
    domain = current_site.domain
    context = {
        "domain": domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "token": token_generator.make_token(user),
        "email": new_email  # новый email передается в контроллер верификации
    }
    message = render_to_string('registration/verify_email.html', context=context)
    email = user.email
    send_email_for_varify_delay.delay(message, email)


@shared_task()
def send_mail_fb(*args, **kwargs):
    send_mail(*args, **kwargs)


