from django.conf.urls import url

from . import views

app_name = "elm"


urlpatterns = [url(r"^$", views.CheckForUpdateView.as_view(), name="check_updates")]
