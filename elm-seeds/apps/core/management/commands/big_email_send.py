import time
from sys import stdout

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Send out email to everyone"

    def handle(self, *args, **options):
        print("Commencing big email send", file=stdout)

        # users = User.objects.filter(is_active=True).exclude(email__contains="qq.com").exclude(email__contains="tom.com")
        users = User.objects.filter(username__in=("pydanny", "audreyr"))

        for index, user in enumerate(users):
            if not user.email.strip():
                continue
            send_mail(
                subject=settings.BIG_EMAIL_SEND_SUBJECT,
                message=settings.BIG_EMAIL_SEND,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            print("Sent to", index, user.email)
            time.sleep(1)
