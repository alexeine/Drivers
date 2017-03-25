from django.db import models

# Create your models here.
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string


def send_email(addresses_to, ctx_dict, subject_template, body_template,
               body_html_template):
    """
    Function that sends an email
    """
    subject = (
        getattr(settings, 'REGISTRATION_EMAIL_SUBJECT_PREFIX', '') +
        render_to_string(
            subject_template, ctx_dict)
    )
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    from_email = getattr(settings, 'REGISTRATION_DEFAULT_FROM_EMAIL',
                         settings.DEFAULT_FROM_EMAIL)
    message_txt = render_to_string(body_template,
                                   ctx_dict)

    email_message = EmailMultiAlternatives(subject, message_txt,
                                           from_email, addresses_to)

    if getattr(settings, 'REGISTRATION_EMAIL_HTML', True):
        try:
            message_html = render_to_string(
                body_html_template, ctx_dict)
        except TemplateDoesNotExist:
            pass
        else:
            email_message.attach_alternative(message_html, 'text/html')

    email_message.send()
