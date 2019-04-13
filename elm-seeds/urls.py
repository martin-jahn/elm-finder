from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout as contrib_logout_view
from django.views.generic.base import TemplateView

from apps.apiv4.viewsets import router
from apps.core.apiv1 import apiv1_gone
from apps.homepage.views import SitemapView, error_404_view, error_500_view, health_check_view, homepage
from apps.package.views import category, python3_list

admin.autodiscover()


urlpatterns = [
    # url(r'^login/\{\{item\.absolute_url\}\}/', RedirectView.as_view(url="/login/github/")),
    url("^auth/", include("social_django.urls", namespace="social")),
    # url('', include('social_auth.urls')),
    url(r"^$", homepage, name="home"),
    url(r"^health_check/$", health_check_view, name="health_check"),
    url(r"^404$", error_404_view, name="404"),
    url(r"^500$", error_500_view, name="500"),
    url(settings.ADMIN_URL_BASE, include(admin.site.urls)),
    url(r"^profiles/", include("apps.profiles.urls")),
    url(r"^packages/", include("apps.package.urls")),
    url(r"^grids/", include("apps.grid.urls")),
    url(r"^feeds/", include("apps.feeds.urls")),
    url(r"^categories/(?P<slug>[-\w]+)/$", category, name="category"),
    url(r"^categories/$", homepage, name="categories"),
    url(r"^python3/$", python3_list, name="py3_compat"),
    # url(regex=r'^login/$', view=TemplateView.as_view(template_name='pages/login.html'), name='login',),
    url(r"^logout/$", contrib_logout_view, {"next_page": "/"}, "logout"),
    # static pages
    url(r"^about/$", TemplateView.as_view(template_name="pages/faq.html"), name="about"),
    url(r"^terms/$", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),
    url(r"^faq/$", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),
    url(r"^syndication/$", TemplateView.as_view(template_name="pages/syndication.html"), name="syndication"),
    url(r"^help/$", TemplateView.as_view(template_name="pages/help.html"), name="help"),
    url(r"^sitemap\.xml$", SitemapView.as_view(), name="sitemap"),
    # new apps
    url(r"^search/", include("apps.searchv2.urls")),
    # apiv2
    # url(r'^api/v2/', include('core.apiv2', namespace="apiv2")),
    # apiv3
    url(r"^api/v3/", include("apps.apiv3.urls", namespace="apiv3")),
    # apiv4
    url(r"^api/v4/", include(router.urls, namespace="apiv4")),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(regex=r"^api/v1/.*$", view=apiv1_gone, name="apiv1_gone"),
    # url(r'^api/v1/', include('core.apiv1', namespace="apitest")),
    # reports
    # url(r'^reports/', include('reports.urls', namespace='reports')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]
