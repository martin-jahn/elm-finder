from django.test import TestCase

from apps.package.tests import initial_data
from apps.searchv2.builders import build_index
from apps.searchv2.models import SearchV2


class BuilderTest(TestCase):
    def setUp(self):
        initial_data.load()

    def test_build_1_count(self):
        self.assertEqual(SearchV2.objects.count(), 0)
        build_index()
        self.assertEqual(SearchV2.objects.count(), 6)
