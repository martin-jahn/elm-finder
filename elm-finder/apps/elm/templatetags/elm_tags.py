from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def shown_users_version(context, package):
    if package.pypi_version() == context["version_data"][package.title]:
        return context["version_data"][package.title]
    else:
        return mark_safe(
            f"<span class='label label-warning'>Old version</span> {context['version_data'][package.title]}"
        )
