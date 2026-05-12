def role_flags(request):
    user = getattr(request, "user", None)
    is_teamleader = False
    if user and getattr(user, "is_authenticated", False):
        try:
            is_teamleader = user.is_superuser or user.groups.filter(name="TeamLeaders").exists()
        except Exception:
            is_teamleader = False
    return {"is_teamleader": is_teamleader}
