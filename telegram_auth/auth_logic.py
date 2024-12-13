from dataclasses import dataclass, asdict

from django.contrib.auth import get_user_model, login
from django.http import HttpRequest

from telegram_auth.models import TelegramToken


User = get_user_model()


@dataclass
class UserInfo:
    id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""


def bound_token_with_user(token: str, user_info: UserInfo) -> None:
    user, created = User.objects.get_or_create(**asdict(user_info))
    if created:
        user.username

    TelegramToken.objects.create(token=token, user=user)


def authenticate_by_token(request: HttpRequest, token: str) -> bool:
    bounded_token = (
        TelegramToken.objects.select_related("user").filter(token=token).last()
    )
    if bounded_token is not None:
        login(request, bounded_token.user)
        bounded_token.delete()
        return True
    return False
