from django.core.mail import send_mail
from django.test import TestCase


def test_email():
    send_mail(
        "테스트 이메일 제목",
        "이것은 테스트 이메일 내용입니다.",
        "junhe0660@gmail.com",
        ["junhe0689@gmail.com"],
        fail_silently=False,
    )
