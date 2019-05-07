from django.contrib import admin

from apps.homepage.models import PSA, Dpotw, Gotw


@admin.register(Dpotw)
class DpotwAdmin(admin.ModelAdmin):
    raw_id_fields = ("package",)


@admin.register(Gotw)
class GotwAdmin(admin.ModelAdmin):
    raw_id_fields = ("grid",)
