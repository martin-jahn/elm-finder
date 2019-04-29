"""views for the :mod:`grid` app"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Count
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from utils.matomo.views import MatomoTrackMixin

from apps.grid.forms import ElementForm, FeatureForm, GridForm, GridPackageForm
from apps.grid.models import Element, Feature, Grid, GridPackage
from apps.package.forms import PackageForm
from apps.package.models import Package
from apps.package.views import repo_data_for_js


def build_element_map(elements):
    # Horrifying two-level dict due to needing to use hash() function later
    element_map = {}
    for element in elements:
        element_map.setdefault(element.feature_id, {})
        element_map[element.feature_id][element.grid_package_id] = element
    return element_map


def grids(request, template_name="grid/grids.html"):
    """lists grids

    Template context:

    * ``grids`` - all grid objects
    """
    # annotations providing bad counts
    grids = Grid.objects.filter()
    grids = grids.prefetch_related("features")
    grids = grids.annotate(gridpackage_count=Count("gridpackage"))
    return render(request, template_name, {"grids": grids})


def grid_detail_landscape(request, slug, template_name="grid/grid_detail2.html"):
    """displays a grid in detail

    Template context:

    * ``grid`` - the grid object
    * ``elements`` - elements of the grid
    * ``features`` - feature set used in the grid
    * ``grid_packages`` - packages involved in the current grid
    """
    grid = get_object_or_404(Grid, slug=slug)
    features = grid.features.all()

    grid_packages = grid.grid_packages.order_by("package__commit_list")

    elements = Element.objects.all().filter(feature__in=features, grid_package__in=grid_packages)

    element_map = build_element_map(elements)

    # These attributes are how we determine what is displayed in the grid
    default_attributes = [
        ("repo_description", "Description"),
        ("category", "Category"),
        ("pypi_downloads", "Downloads"),
        ("last_updated", "Last Updated"),
        ("pypi_version", "Version"),
        ("repo", "Repo"),
        ("commits_over_52", "Commits"),
        ("repo_watchers", "Stars"),
        ("repo_forks", "Forks"),
        ("participant_list", "Participants"),
        ("license_latest", "License"),
    ]

    return render(
        request,
        template_name,
        {
            "grid": grid,
            "features": features,
            "grid_packages": grid_packages,
            "attributes": default_attributes,
            "elements": element_map,
        },
    )


class AddGridView(FormView):
    template_name = "grid/update_grid.html"
    form_class = GridForm

    def get_page_title(self, context):
        return f"Grid / Add"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.can_add_grid:
            return HttpResponseForbidden("permission denied")
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        new_grid = form.save()
        return redirect("grid", slug=new_grid.slug)


@login_required
def edit_grid(request, slug, template_name="grid/update_grid.html"):
    """View to modify the grid, handles GET and POST requests.
    This view requires user to be logged in.

    Template context:

    * ``form`` - instance of :class:`grid.forms.GridForm`
    """

    if not request.user.profile.can_edit_grid:
        return HttpResponseForbidden("permission denied")

    grid = get_object_or_404(Grid, slug=slug)
    form = GridForm(request.POST or None, instance=grid)

    if form.is_valid():
        grid = form.save()
        message = "Grid has been edited"
        messages.add_message(request, messages.INFO, message)
        return HttpResponseRedirect(reverse("grid", kwargs={"slug": grid.slug}))
    return render(request, template_name, {"form": form, "grid": grid})


@login_required
def add_feature(request, grid_slug, template_name="grid/update_feature.html"):
    """Adds a feature to the grid, accepts GET and POST requests.

    Requires user to be logged in

    Template context:

    * ``form`` - instance of :class:`grid.forms.FeatureForm` form
    * ``grid`` - instance of :class:`grid.models.Grid` model
    """

    if not request.user.profile.can_add_grid_feature:
        return HttpResponseForbidden("permission denied")

    grid = get_object_or_404(Grid, slug=grid_slug)
    form = FeatureForm(request.POST or None)

    if form.is_valid():
        feature = form.save(commit=False)
        feature.grid = grid
        feature.save()
        return HttpResponseRedirect(reverse("grid", kwargs={"slug": feature.grid.slug}))

    return render(request, template_name, {"form": form, "grid": grid})


@login_required
def edit_feature(request, id, template_name="grid/update_feature.html"):
    """edits feature on a grid - this view has the same
    semantics as :func:`grid.views.add_feature`.

    Requires the user to be logged in.
    """

    if not request.user.profile.can_edit_grid_feature:
        return HttpResponseForbidden("permission denied")

    feature = get_object_or_404(Feature, id=id)
    form = FeatureForm(request.POST or None, instance=feature)

    if form.is_valid():
        feature = form.save()
        return HttpResponseRedirect(reverse("grid", kwargs={"slug": feature.grid.slug}))

    return render(request, template_name, {"form": form, "grid": feature.grid})


@permission_required("grid.delete_feature")
def delete_feature(request, id, template_name="grid/edit_feature.html"):
    # do not need to check permission via profile because
    # we default to being strict about deleting
    """deletes a feature from the grid, ``id`` is id of the
    :class:`grid.models.Feature` model that is to be deleted

    Requires permission `grid.delete_feature`.

    Redirects to the parent :func:`grid.views.grid_detail`
    """

    feature = get_object_or_404(Feature, id=id)
    Element.objects.filter(feature=feature).delete()
    feature.delete()

    return HttpResponseRedirect(reverse("grid", kwargs={"slug": feature.grid.slug}))


@permission_required("grid.delete_gridpackage")
def delete_grid_package(request, id, template_name="grid/edit_feature.html"):
    """Deletes package from the grid, ``id`` is the id of the
    :class:`grid.models.GridPackage` instance

    Requires permission ``grid.delete_gridpackage``.

    Redirects to :func:`grid.views.grid_detail`.
    """

    # do not need to check permission via profile because
    # we default to being strict about deleting
    package = get_object_or_404(GridPackage, id=id)
    Element.objects.filter(grid_package=package).delete()
    package.delete()

    return HttpResponseRedirect(reverse("grid", kwargs={"slug": package.grid.slug}))


@login_required
def edit_element(request, feature_id, package_id, template_name="grid/edit_element.html"):

    if not request.user.profile.can_edit_grid_element:
        return HttpResponseForbidden("permission denied")

    feature = get_object_or_404(Feature, pk=feature_id)
    grid_package = get_object_or_404(GridPackage, pk=package_id)

    # Sanity check to make sure both the feature and grid_package are related to
    # the same grid!
    if feature.grid_id != grid_package.grid_id:
        raise Http404

    element, created = Element.objects.get_or_create(grid_package=grid_package, feature=feature)

    form = ElementForm(request.POST or None, instance=element)

    if form.is_valid():
        element = form.save()
        return HttpResponseRedirect(reverse("grid", kwargs={"slug": feature.grid.slug}))

    return render(
        request,
        template_name,
        {"form": form, "feature": feature, "package": grid_package.package, "grid": feature.grid},
    )


@login_required
def add_grid_package(request, grid_slug, template_name="grid/add_grid_package.html"):
    """Add an existing package to this grid."""

    if not request.user.profile.can_add_grid_package:
        return HttpResponseForbidden("permission denied")

    grid = get_object_or_404(Grid, slug=grid_slug)
    grid_package = GridPackage()
    form = GridPackageForm(request.POST or None, instance=grid_package)

    if form.is_valid():
        package = get_object_or_404(Package, id=request.POST["package"])
        try:
            GridPackage.objects.get(grid=grid, package=package)
            message = "Sorry, but '%s' is already in this grid." % package.title
            messages.add_message(request, messages.ERROR, message)
        except GridPackage.DoesNotExist:
            grid_package = GridPackage(grid=grid, package=package)
            grid_package.save()
            redirect = request.POST.get("redirect", "")
            if redirect:
                return HttpResponseRedirect(redirect)

            return HttpResponseRedirect(reverse("grid", kwargs={"slug": grid.slug}))

    return render(request, template_name, {"form": form, "grid": grid})


@login_required
def add_new_grid_package(request, grid_slug, template_name="package/package_form.html"):
    """Add a package to a grid that isn't yet represented on the site."""

    if not request.user.profile.can_add_grid_package:
        return HttpResponseForbidden("permission denied")

    grid = get_object_or_404(Grid, slug=grid_slug)

    new_package = Package()
    form = PackageForm(request.POST or None, instance=new_package)

    if form.is_valid():
        new_package = form.save()
        GridPackage.objects.create(grid=grid, package=new_package)
        return HttpResponseRedirect(reverse("grid", kwargs={"slug": grid_slug}))

    return render(request, template_name, {"form": form, "repo_data": repo_data_for_js(), "action": "add"})


class AjaxGridListView(TemplateView):
    template_name = "grid/ajax_grid_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get("q", "")
        grids = []
        if q:
            grids = Grid.objects.filter(title__istartswith=q)
            package_id = self.request.GET.get("package_id", "")
            if package_id:
                grids = grids.exclude(gridpackage__package__id=package_id)

        context["grids"] = grids
        return context


class GridDetailView(MatomoTrackMixin, TemplateView):
    template_name = "grid/grid_detail.html"

    def get_page_title(self, context):
        return f'Grid / {context["grid"].title}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grid = get_object_or_404(Grid, slug=kwargs["slug"])
        features = grid.features.select_related(None)

        grid_packages = grid.grid_packages.order_by("-package__repo_watchers")

        elements = Element.objects.filter(feature__in=features, grid_package__in=grid_packages)

        element_map = build_element_map(elements)

        # These attributes are how we determine what is displayed in the grid
        default_attributes = [
            ("repo_description", "Description"),
            ("category", "Category"),
            ("pypi_downloads", "Downloads"),
            ("last_updated", "Last Updated"),
            ("pypi_version", "Version"),
            ("repo", "Repo"),
            ("commits_over_52", "Commits"),
            ("repo_watchers", "Stars"),
            ("repo_forks", "Forks"),
            ("participant_list", "Participants"),
            ("license_latest", "License"),
        ]

        context.update(
            {
                "grid": grid,
                "features": features,
                "grid_packages": grid_packages,
                "attributes": default_attributes,
                "elements": element_map,
            }
        )

        return context


class GridListAPIView(ListAPIView):
    model = Grid
    paginate_by = 20


class GridDetailAPIView(RetrieveAPIView):
    model = Grid


class GridTimesheetView(MatomoTrackMixin, TemplateView):
    template_name = "grid/grid_timesheet.html"

    def get_page_title(self, context):
        return f'Grid / {context["grid"].title} / Timesheet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grid = get_object_or_404(Grid, slug=kwargs["slug"])
        grid_packages = grid.grid_packages.order_by("-package__modified").select_related()
        context.update({"grid": grid, "grid_packages": grid_packages})

        return context
