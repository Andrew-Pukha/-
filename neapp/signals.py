from django.core.exceptions import ValidationError, PermissionDenied
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed

from django.shortcuts import render
from django.utils import timezone

from .models import *
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, request



def send_notifications(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/neapp/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [subs.email for subs in subscribers]
            subscribers_emails = set(subscribers_emails)

        send_notifications(instance.preview, instance.pk, instance.post_title, instance.subscribers_emails)

