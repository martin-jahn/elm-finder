from django.contrib import admin
from reversion.admin import VersionAdmin

from apps.grid.models import Element, Feature, Grid, GridPackage


class GridPackageInline(admin.TabularInline):
    model = GridPackage
    raw_id_fields = "grid", "package"


@admin.register(Grid)
class GridAdmin(VersionAdmin):
    list_display_links = ("title",)
    list_display = ("title", "header")
    list_editable = ("header",)
    inlines = [GridPackageInline]


@admin.register(Element)
class ElementAdmin(VersionAdmin):
    raw_id_fields = ("grid_package", "feature")


@admin.register(Feature)
class FeatureAdmin(VersionAdmin):
    raw_id_fields = ("grid",)


@admin.register(GridPackage)
class GridPackageAdmin(VersionAdmin):
    raw_id_fields = ("grid", "package")
