"""grid url patterns"""
from django.conf.urls import url

from apps.grid import views

urlpatterns = [
    url(r"^add/$", view=views.add_grid, name="add_grid"),
    url(r"^(?P<slug>[-\w]+)/edit/$", view=views.edit_grid, name="edit_grid"),
    url(r"^element/(?P<feature_id>\d+)/(?P<package_id>\d+)/$", view=views.edit_element, name="edit_element"),
    url(r"^feature/add/(?P<grid_slug>[a-z0-9\-_]+)/$", view=views.add_feature, name="add_feature"),
    url(r"^feature/(?P<id>\d+)/$", view=views.edit_feature, name="edit_feature"),
    url(r"^feature/(?P<id>\d+)/delete/$", view=views.delete_feature, name="delete_feature"),
    url(r"^package/(?P<id>\d+)/delete/$", view=views.delete_grid_package, name="delete_grid_package"),
    url(r"^(?P<grid_slug>[a-z0-9\-_]+)/package/add/$", view=views.add_grid_package, name="add_grid_package"),
    url(r"^(?P<grid_slug>[a-z0-9\-_]+)/package/add/new$", view=views.add_new_grid_package, name="add_new_grid_package"),
    url(r"^ajax_grid_list/$", view=views.AjaxGridListView.as_view(), name="ajax_grid_list"),
    url(r"^$", view=views.grids, name="grids"),
    url(r"^g/(?P<slug>[-\w]+)/$", view=views.GridDetailView.as_view(), name="grid"),
    url(r"^g/(?P<slug>[-\w]+)/landscape/$", view=views.grid_detail_landscape, name="grid_landscape"),
    url(r"^g/(?P<slug>[-\w]+)/timesheet/$", view=views.GridTimesheetView.as_view(), name="grid_timesheet"),
]
