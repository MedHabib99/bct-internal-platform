from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from .models import EmailOTP
from .utils import send_otp_email

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, "Invalid username or password.")
            return render(request, "accounts/login.html")

        otp = EmailOTP.create_for_user(
            user,
            ip=request.META.get("REMOTE_ADDR"),
            ua=request.META.get("HTTP_USER_AGENT", "")
        )
        try:
            send_otp_email(user.email, otp.code)
        except Exception:
            messages.error(request, "Could not send the OTP email. Please try again.")
            return render(request, "accounts/login.html")

        request.session["pending_uid"] = user.pk
        messages.info(request, "We sent a 6-digit code to your email.")
        return redirect("accounts:otp_verify")

    return render(request, "accounts/login.html")


@require_http_methods(["GET", "POST"])
def otp_verify_view(request):
    pending_uid = request.session.get("pending_uid")
    if not pending_uid:
        messages.error(request, "Start by logging in.")
        return redirect("accounts:login")

    User = get_user_model()
    try:
        user = User.objects.get(pk=pending_uid)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect("accounts:login")

    try:
        otp = EmailOTP.objects.filter(user=user, consumed_at__isnull=True).latest("created_at")
    except EmailOTP.DoesNotExist:
        messages.error(request, "No active code. Please log in again.")
        return redirect("accounts:login")

    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        otp.attempts += 1
        otp.save(update_fields=["attempts"])
        if otp.attempts > 5:
            otp.delete()
            messages.error(request, "Too many attempts. Please log in again.")
            return redirect("accounts:login")

        if otp.is_expired():
            otp.delete()
            messages.error(request, "Code expired. Please log in again.")
            return redirect("accounts:login")

        if code == otp.code:
            otp.consume()
            login(request, user)
            request.session.pop("pending_uid", None)
            messages.success(request, "Logged in successfully.")
            return redirect("home")

        messages.error(request, "Incorrect code.")

    return render(request, "accounts/otp_verify.html")
