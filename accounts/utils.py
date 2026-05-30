from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


email_verification_token = PasswordResetTokenGenerator()

def send_verification_email(user):

    token = email_verification_token.make_token(user)

    verification_link = (
        f"http://127.0.0.1:8000/api/verify-email/"
        f"{user.id}/{token}/"
    )

    send_mail(
        subject="Verify Your Account",
        message=f"Click this link:\n{verification_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )