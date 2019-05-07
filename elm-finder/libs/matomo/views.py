import time

from django.conf import settings

from libs.matomo.tasks import send_to_matomo


class MatomoTrackMixin:
    def get_page_title(self, context):
        raise NotImplementedError()

    def render_to_response(self, context, **response_kwargs):
        self.process_view(context)
        return super().render_to_response(context, **response_kwargs)

    def process_view(self, context):
        page_title = self.get_page_title(context)
        self.track_view(page_title)

    def track_view(self, page_title, **kwargs):
        self.tracking_data = {
            "page_title": page_title,
            "user_agent": self.request.headers.get("user-agent"),
            "language": self.request.headers.get("accept-language"),
            "referer": self.request.headers.get("referer"),
            "ip": self.request.META.get("REMOTE_ADDR"),
            "country": self.request.META.get("HTTP_CF_IPCOUNTRY"),
            "url": f"https://{settings.DOMAIN}{self.request.get_full_path()}",
            "extra": kwargs,
        }

    def dispatch(self, request, *args, **kwargs):
        self.tracking_data = None
        start_time = time.time()

        response = super().dispatch(request, *args, **kwargs)

        if self.tracking_data is not None:
            request_time = int((time.time() - start_time) * 1000)
            send_to_matomo.delay(self.tracking_data, request_time)

        return response
