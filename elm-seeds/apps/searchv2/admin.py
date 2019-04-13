from django.contrib import admin

from apps.searchv2.models import SearchV2


class SearchV2Admin(admin.ModelAdmin):

    search_fields = ("title", "title_no_prefix")


admin.site.register(SearchV2, SearchV2Admin)
