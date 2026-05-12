from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(to_email: str, code: str) -> None:
    subject = "Your BCT login code"
    body = (
        f"Your one-time code is: {code}\n"
        f"It expires in 5 minutes.\n"
        f"If you did not request it, you can ignore this email."
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=False)
