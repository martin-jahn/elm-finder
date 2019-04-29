from django.conf import settings
from utils.matomo.tasks import send_to_matomo


class MatomoTrackMixin:
    def get_page_title(self, context):
        raise NotImplementedError()

    def render_to_response(self, context, **response_kwargs):
        self.track_view(context)
        return super().render_to_response(context, **response_kwargs)

    def track_view(self, context):
        page_title = self.get_page_title(context)
        user_agent = self.request.headers.get("user-agent")
        language = self.request.headers.get("accept-language")
        referer = self.request.headers.get("referer")
        ip = self.request.META.get("REMOTE_ADDR")
        url = f"https://{settings.DOMAIN}{self.request.path}"

        send_to_matomo.delay(
            ip=ip, page_url=url, user_agent=user_agent, page_title=page_title, referer=referer, language=language
        )
