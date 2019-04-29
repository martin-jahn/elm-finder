from django.conf.urls import url

from apps.homepage.views import HomepageView
from apps.searchv2 import views

urlpatterns = [
    url(regex="^build$", view=views.build_search, name="build_search"),
    url(regex="^$", view=HomepageView.as_view(template_name="searchv2/search.html"), name="search"),
    url(regex="^packages/autocomplete/$", view=views.search_packages_autocomplete, name="search_packages_autocomplete"),
]
