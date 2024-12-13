import json
from telegram import Update

from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from telegram_auth.bot import bot, dp
from telegram_auth.auth_logic import authenticate_by_token


@csrf_exempt
def webhook_handler(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        update = Update.de_json(json.loads(request.body), bot)
        dp.process_update(update)

    return HttpResponse(status=200)


@require_http_methods(["POST"])
def auth(request: HttpRequest) -> HttpResponse:
    body = json.loads(request.body)
    auth_token = body.get("auth_token")
    if auth_token is None:
        return HttpResponse(status=400)
    authenticated = authenticate_by_token(request, auth_token)
    if not authenticated:
        return HttpResponse(status=401)
    return HttpResponse(status=200)
