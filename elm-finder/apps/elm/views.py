from django.views.generic import FormView

from apps.elm.forms import UpdateForm
from apps.package.models import Package
from libs.matomo.views import MatomoTrackMixin


class CheckForUpdateView(MatomoTrackMixin, FormView):
    template_name = "elm/check_updates.html"
    form_class = UpdateForm

    def get_page_title(self, context):
        return "Elm update checker"

    def form_valid(self, form):
        data = form.cleaned_data["elm_json"]

        version_data = data["dependencies"]["direct"]
        version_data.update(data["dependencies"].get("indirect", {}))

        if "test-dependencies" in data:
            version_data.update(data["test-dependencies"].get("direct", {}))
            version_data.update(data["test-dependencies"].get("indirect", {}))

        packages = Package.objects.filter(title__in=version_data.keys())
        return self.get(self.request, version_data=version_data, packages=packages, form=form)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
