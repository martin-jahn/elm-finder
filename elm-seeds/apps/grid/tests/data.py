from django.contrib.auth.models import User
from utils.tests import load as utils_load

from apps.profiles.models import Profile


def load():
    utils_load()

    for user in User.objects.all():
        profile = Profile.objects.create(user=user)
