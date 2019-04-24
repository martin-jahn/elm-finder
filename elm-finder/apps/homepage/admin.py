from django.contrib import admin

from apps.homepage.models import PSA, Dpotw, Gotw

admin.site.register(Dpotw)
admin.site.register(Gotw)
admin.site.register(PSA)
