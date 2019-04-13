from django.contrib import admin

from apps.homepage.models import Dpotw, Gotw, PSA

admin.site.register(Dpotw)
admin.site.register(Gotw)
admin.site.register(PSA)
