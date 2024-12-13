import secrets

from django.views.generic.base import TemplateView
from django.conf import settings

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


class IndexView(TemplateView):
    template_name = "index.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        if not self.request.user.is_authenticated:
            context["token"] = secrets.token_urlsafe(24)
            context["bot_name"] = settings.TELEGRAM_BOT_NAME
        return context
