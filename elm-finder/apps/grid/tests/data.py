from django.contrib.auth.models import User

from apps.profiles.models import Profile
from libs.tests import load as utils_load


def load():
    utils_load()

    for user in User.objects.all():
        profile = Profile.objects.create(user=user)
