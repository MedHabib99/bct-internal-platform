from django.shortcuts import redirect, render
from django.urls import reverse

class AdminRoleRequiredMiddleware:
    ALLOWED_ADMIN_ENDPOINTS = ("/admin/login/", "/admin/logout/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith("/admin/") and request.user.is_authenticated:
            if not any(path.startswith(p) for p in self.ALLOWED_ADMIN_ENDPOINTS):
                if not getattr(request.user, "is_superuser", False):
                    return render(request, "no_admin_access.html", status=403)

        return self.get_response(request)
