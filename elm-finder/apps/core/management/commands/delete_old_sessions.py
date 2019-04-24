from datetime import datetime

from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Delete old sessions"

    def handle_noargs(self, **options):
        old_sessions = Session.objects.filter(expire_date__lt=datetime.now())

        self.stdout.write("Deleting {0} expired sessions".format(old_sessions.count()))

        for index, session in enumerate(old_sessions[:10000]):
            session.delete()

        self.stdout.write(
            "{0} expired sessions remaining".format(Session.objects.filter(expire_date__lt=datetime.now()).count())
        )
