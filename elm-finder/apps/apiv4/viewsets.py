from rest_framework import mixins, routers, viewsets
from rest_framework.response import Response

from apps.grid.models import Grid
from apps.package.models import Category, Package
from apps.searchv2.models import SearchV2
from apps.searchv2.views import search_function
from libs.matomo.views import MatomoTrackMixin

from .serializers import CategorySerializer, GridSerializer, PackageSerializer, SearchV2Serializer


class SearchV2ViewSet(MatomoTrackMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Accepts a 'q' GET parameter. Results are currently sorted only by
        their weight.
    """

    serializer_class = SearchV2Serializer
    queryset = SearchV2.objects.all()

    def list(self, request):
        qr = request.GET.get("q", "")

        search_qs = search_function(qr)
        search_count = search_qs.count()
        queryset = search_qs[:20]

        serializer = SearchV2Serializer(queryset, many=True)

        self.track_view("Search View", search_count=search_count, search=qr)
        return Response(serializer.data)


class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows packages to be viewed or edited.
    """

    queryset = Package.objects.all().order_by("-id")
    serializer_class = PackageSerializer
    paginate_by = 20


class GridViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grid.objects.all().order_by("-id")
    serializer_class = GridSerializer
    paginate_by = 20


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer
    paginate_by = 20


router = routers.DefaultRouter()
router.register(r"packages", PackageViewSet)
router.register(r"search", SearchV2ViewSet)
router.register(r"grids", GridViewSet)
router.register(r"categories", CategoryViewSet)
