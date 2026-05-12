from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import make_aware

from .forms import FeedbackForm, FeedbackReplyForm, StatusUpdateForm
from .models import Feedback, FeedbackReply


def is_teamleader(user):
    try:
        if not getattr(user, "is_authenticated", False):
            return False
        if getattr(user, "is_superuser", False):
            return True
        return user.groups.filter(name="TeamLeaders").exists()
    except Exception:
        return False


def teamleader_required(view_func):
    return login_required(user_passes_test(is_teamleader)(view_func))


@login_required
def index(request):
    if is_teamleader(request.user):
        return redirect("feedback:admin_list")
    return redirect("feedback:my_list")

@login_required
def create(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            fb = form.save(commit=False)
            if not form.cleaned_data.get("is_anonymous"):
                fb.created_by = request.user
            fb.save()

            trackers = set(request.session.get("feedback_trackers", []))
            trackers.add(str(fb.tracker))
            request.session["feedback_trackers"] = list(trackers)

            messages.success(request, "Thanks! Your feedback has been submitted.")
            return redirect("feedback:thanks")
    else:
        form = FeedbackForm()
    return render(request, "feedback/form.html", {"form": form})


@login_required
def thanks(request):
    return render(request, "feedback/thanks.html")


@login_required
def my_list(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    trackers = request.session.get("feedback_trackers", [])
    qs_user = Feedback.objects.filter(created_by=request.user)
    qs_trk = Feedback.objects.filter(tracker__in=trackers)
    qs = (qs_user | qs_trk).distinct()

    if date_from:
        try:
            dt_from = make_aware(datetime.strptime(date_from, "%Y-%m-%d"))
            qs = qs.filter(created_at__gte=dt_from)
        except Exception:
            messages.error(request, "Invalid start date format. Use YYYY-MM-DD.")
    if date_to:
        try:
            dt_to = make_aware(datetime.strptime(date_to, "%Y-%m-%d")).replace(hour=23, minute=59, second=59)
            qs = qs.filter(created_at__lte=dt_to)
        except Exception:
            messages.error(request, "Invalid end date format. Use YYYY-MM-DD.")

    items = qs.select_related("created_by").order_by("-created_at")
    return render(
        request,
        "feedback/my_list.html",
        {"items": items, "date_from": date_from, "date_to": date_to},
    )


@login_required
def detail(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    trackers = request.session.get("feedback_trackers", [])

    allowed = (
        is_teamleader(request.user)
        or (fb.created_by_id == request.user.id and not fb.is_anonymous)
        or (str(fb.tracker) in trackers)
    )
    if not allowed:
        messages.error(request, "You do not have permission to view that feedback.")
        return redirect("feedback:my_list")

    reply_form = FeedbackReplyForm()
    status_form = StatusUpdateForm(initial={"status": fb.status})
    return render(
        request,
        "feedback/detail.html",
        {
            "item": fb,
            "reply_form": reply_form,
            "status_form": status_form,
        },
    )


@teamleader_required
def admin_list(request):
    qs = Feedback.objects.select_related("created_by")

    status = request.GET.get("status")
    category = request.GET.get("category")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if status:
        qs = qs.filter(status=status)
    if category:
        qs = qs.filter(category=category)
    if date_from:
        try:
            dt_from = make_aware(datetime.strptime(date_from, "%Y-%m-%d"))
            qs = qs.filter(created_at__gte=dt_from)
        except Exception:
            messages.error(request, "Invalid start date format. Use YYYY-MM-DD.")
    if date_to:
        try:
            dt_to = make_aware(datetime.strptime(date_to, "%Y-%m-%d")).replace(hour=23, minute=59, second=59)
            qs = qs.filter(created_at__lte=dt_to)
        except Exception:
            messages.error(request, "Invalid end date format. Use YYYY-MM-DD.")

    items = qs.order_by("-created_at")
    return render(
        request,
        "feedback/admin_list.html",
        {
            "items": items,
            "status": status,
            "category": category,
            "date_from": date_from,
            "date_to": date_to,
        },
    )


@teamleader_required
def admin_set_status(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            fb.status = form.cleaned_data["status"]
            fb.save()
            messages.success(request, f"Status updated to {fb.get_status_display()}.")
        else:
            messages.error(request, "Invalid status.")
    return redirect(reverse("feedback:detail", args=[pk]))


@teamleader_required
def admin_reply(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        form = FeedbackReplyForm(request.POST)
        if form.is_valid():
            FeedbackReply.objects.create(
                feedback=fb,
                author=request.user,
                message=form.cleaned_data["message"],
            )
            messages.success(request, "Reply posted.")
        else:
            messages.error(request, "Reply cannot be empty.")
    return redirect(reverse("feedback:detail", args=[pk]))
