from django.conf.urls import url
from django.views.generic import RedirectView
from django.views.generic.dates import ArchiveIndexView

from apps.package.models import Package
from apps.package.views import (
    DocView,
    PackageDetailView,
    PackageDocsView,
    PackageListView,
    add_example,
    add_package,
    ajax_package_list,
    confirm_delete_example,
    delete_example,
    edit_documentation,
    edit_example,
    edit_package,
    github_webhook,
    post_data,
    update_package,
    usage,
)

urlpatterns = [
    url(regex=r"^$", view=PackageListView.as_view(), name="packages"),
    url(
        regex=r"^latest/$",
        view=ArchiveIndexView.as_view(
            queryset=Package.objects.filter().select_related(), paginate_by=50, date_field="created"
        ),
        name="latest_packages",
    ),
    url(regex="^add/$", view=add_package, name="add_package"),
    url(regex="^(?P<slug>[-\w]+)/edit/$", view=edit_package, name="edit_package"),
    url(regex="^(?P<slug>[-\w]+)/fetch-data/$", view=update_package, name="fetch_package_data"),
    url(regex="^(?P<slug>[-\w]+)/post-data/$", view=post_data, name="post_package_data"),
    url(regex="^(?P<slug>[-\w]+)/example/add/$", view=add_example, name="add_example"),
    url(regex="^(?P<slug>[-\w]+)/example/(?P<id>\d+)/edit/$", view=edit_example, name="edit_example"),
    url(regex="^(?P<slug>[-\w]+)/example/(?P<id>\d+)/delete/$", view=delete_example, name="delete_example"),
    url(
        regex="^(?P<slug>[-\w]+)/example/(?P<id>\d+)/confirm_delete/$",
        view=confirm_delete_example,
        name="confirm_delete_example",
    ),
    url(regex="^p/(?P<slug>[-\w]+)/$", view=RedirectView.as_view(pattern_name="package", permanent=True)),
    url(
        regex="^(?P<slug>[-\w]+)/docs$",
        view=RedirectView.as_view(pattern_name="docs", permanent=True),
        kwargs={"version": "latest"},
    ),
    url(regex="^(?P<slug>[-\w]+)/docs/(?P<version>[-\w.]+)/$", view=PackageDocsView.as_view(), name="docs"),
    url(regex="^(?P<slug>[-\w]+)/docs/(?P<version>[-\w.]+)/(?P<title>[-\w.]+)/$", view=DocView.as_view(), name="docs"),
    url(regex="^(?P<slug>[-\w]+)/$", view=PackageDetailView.as_view(), name="package"),
    url(regex="^ajax_package_list/$", view=ajax_package_list, name="ajax_package_list"),
    url(regex="^usage/(?P<slug>[-\w]+)/(?P<action>add|remove)/$", view=usage, name="usage"),
    url(regex="^(?P<slug>[-\w]+)/document/$", view=edit_documentation, name="edit_documentation"),
    url(regex="^github-webhook/$", view=github_webhook, name="github_webhook"),
]
