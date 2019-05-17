from datetime import datetime
from time import sleep

import markdown
import requests
from django.core.management import BaseCommand
from django.db import transaction
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from tqdm import tqdm

from apps.package.models import Category, Package, Version


class Command(BaseCommand):
    HORIZONTAL_LINE = "-" * 10
    DOCS_IDENTIFIER = "@docs"

    help = "Download documentation for Elm libraries"

    def compile_alias(self, data, item_name):
        item = data[item_name]["item"]
        args = " ".join(item.get("args", []))
        return f"""
<span id="{item_name}"></span>
###type alias [{item_name}](#{item_name}) {args} =
{item['type']}

{item['comment']}

{self.HORIZONTAL_LINE}
"""

    def compile_value(self, data, item_name):
        item = data[item_name]["item"]
        return f"""

<span id="{item_name}"></span>
###[{item_name}](#{item_name}) : {item['type']}

{item['comment']}

{self.HORIZONTAL_LINE}
"""

    def compile_union(self, data, item_name):
        item = data[item_name]["item"]
        args = " ".join(item.get("args", []))
        if item.get("cases"):
            return f"""

<span id="{item_name}"></span>
###type [{item_name}](#{item_name}) {args} 
= {item_name}

{item['cases']}

{item['comment']}

{self.HORIZONTAL_LINE}
        """
        else:
            return f"""

<span id="{item_name}"></span>
###type [{item_name}](#{item_name}) {args}

{item['cases']}

{item['comment']}

{self.HORIZONTAL_LINE}
        """

    def process_docs(self, package, version):
        r = requests.get(f"https://package.elm-lang.org/packages/{package.title}/{version.number}/docs.json")
        r.raise_for_status()

        for idx, page in enumerate(r.json()):
            doc, created = version.docs.get_or_create(title=page["name"], encoded_content=page, order=idx + 1)

            if created:
                data = {item["name"]: {"item": item, "type": "alias"} for item in page["aliases"]}
                data.update({item["name"]: {"item": item, "type": "union"} for item in page["unions"]})
                data.update({item["name"]: {"item": item, "type": "value"} for item in page["values"]})
                data.update({item["name"]: {"item": item, "type": "binop"} for item in page["binops"]})

                lines = page["comment"].split("\n")
                processed_lines = []

                i = 0
                while i < len(lines):
                    processed_lines.append(lines[i])

                    if lines[i].startswith(self.DOCS_IDENTIFIER) and lines[i].endswith(","):
                        while lines[i] != "":
                            i += 1
                            processed_lines[-1] += lines[i][1:]

                    i += 1

                compiled_doc = []
                for line in processed_lines:
                    if line.startswith(self.DOCS_IDENTIFIER):
                        compiled_doc.append(self.HORIZONTAL_LINE)

                        for item in line[6:].split(", "):
                            item = item.strip()
                            if item.startswith("(") and item.endswith(")"):
                                item = item[1:-1]
                            if " " in item:
                                for part in item.split(" "):
                                    compiled_doc.append(self.render_item(data, part, version))
                            if "," in item:
                                for part in item.split(","):
                                    compiled_doc.append(self.render_item(data, part, version))
                            else:
                                compiled_doc.append(self.render_item(data, item, version))
                    else:
                        compiled_doc.append(line)

                doc.content = self.render_markdown("\n".join(compiled_doc))
                doc.save()

    def render_item(self, data, item, version):
        if item not in data:
            print(item, version)
            return ""

        if data[item]["type"] == "alias":
            return self.compile_alias(data, item)
        elif data[item]["type"] == "value" or data[item]["type"] == "binop":
            return self.compile_value(data, item)
        elif data[item]["type"] == "union":
            return self.compile_union(data, item)
        else:
            raise NotImplementedError(data[item]["type"])

    def render_markdown(self, text):
        return markdown.markdown(
            text, extensions=[CodeHiliteExtension(linenums=False, noclasses=True), FencedCodeExtension()]
        )

    def update_versions(self, package):
        r = requests.get(f"https://package.elm-lang.org/packages/{package.title}/releases.json")
        r.raise_for_status()

        version = package.versions.first()

        for number, timestamp_released in r.json().items():
            Version.objects.update_or_create(
                package=package,
                number=number,
                defaults={"license": version.license, "upload_time": datetime.utcfromtimestamp(timestamp_released)},
            )

    def handle(self, *args, **options):
        category = Category.objects.get(slug="libraries")
        packages = Package.objects.filter(category=category).order_by("id")

        for package in tqdm(packages.iterator(), total=packages.count()):
            self.update_versions(package)

            for version in package.versions.filter(readme__isnull=True):
                with transaction.atomic():
                    r = requests.get(
                        f"https://package.elm-lang.org/packages/{package.title}/{version.number}/README.md"
                    )
                    r.raise_for_status()

                    version.encoded_readme = r.text
                    version.readme = self.render_markdown(version.encoded_readme)
                    version.save()

                    self.process_docs(package, version)

                sleep(1)
