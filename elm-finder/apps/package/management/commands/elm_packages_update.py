import requests
from django.core.management import BaseCommand
from django.utils.text import slugify
from tqdm import tqdm

from apps.package.models import Category, Package, Version


class Command(BaseCommand):

    help = "Updates all the packages from package.elm-lang.org. Commands belongs to django-packages.package"

    def handle(self, *args, **options):
        r = requests.get("https://package.elm-lang.org/search.json")
        r.raise_for_status()
        category = Category.objects.get(slug="libraries")

        for package in tqdm(r.json()):
            github_url = f'https://github.com/{package["name"]}'
            elm_packages_url = f'https://package.elm-lang.org/packages/{package["name"]}/latest/'
            slug = slugify(package["name"].replace("/", "-"))

            pkg, _ = Package.objects.update_or_create(
                repo_url=github_url,
                defaults={
                    "title": package["name"],
                    "slug": slug,
                    "category": category,
                    "repo_description": package["summary"],
                    "documentation_url": elm_packages_url,
                },
            )

            for version in package["versions"]:
                Version.objects.get_or_create(package=pkg, number=version, defaults={"license": package["license"]})
