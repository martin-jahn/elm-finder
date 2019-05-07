from django.contrib import admin
from reversion.admin import VersionAdmin

from apps.package.models import Category, Commit, Package, PackageExample, Version


@admin.register(Category)
class CategoryAdmin(VersionAdmin):
    list_display = "title", "title_plural"


class PackageExampleInline(admin.TabularInline):
    model = PackageExample
    raw_id_fields = ("created_by",)


@admin.register(Package)
class PackageAdmin(VersionAdmin):

    save_on_top = True
    search_fields = ("title",)
    list_filter = ("category",)
    list_display = ("title", "created")
    date_hierarchy = "created"
    inlines = [PackageExampleInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "pypi_url",
                    "repo_url",
                    "usage",
                    "created_by",
                    "last_modified_by",
                )
            },
        ),
        (
            "Pulled data",
            {
                "classes": ("collapse",),
                "fields": (
                    "repo_description",
                    "repo_watchers",
                    "repo_forks",
                    "commit_list",
                    "pypi_downloads",
                    "participants",
                ),
            },
        ),
    )
    raw_id_fields = "category", "created_by", "last_modified_by", "usage"


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ("package", "commit_date", "commit_hash")
    raw_id_fields = ("package",)


@admin.register(Version)
class VersionLocalAdmin(admin.ModelAdmin):
    search_fields = ("package__title",)
    raw_id_fields = ("package",)


@admin.register(PackageExample)
class PackageExampleAdmin(admin.ModelAdmin):

    list_display = ("title", "active")
    search_fields = ("title",)

    raw_id_fields = "package", "created_by"
