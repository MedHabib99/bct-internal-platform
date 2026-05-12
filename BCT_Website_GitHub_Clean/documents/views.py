from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Document
from .forms import DocumentForm


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__iexact="Teamleader").exists()
        )
    )


class TeamleaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_teamleader(self.request.user)


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = "documents/list.html"
    context_object_name = "documents"
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        qs = Document.objects.all()
        if not is_teamleader(self.request.user):
            qs = qs.filter(visibility=Document.VISIBLE_ALL)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["is_teamleader"] = is_teamleader(self.request.user)
        return ctx


class DocumentCreateView(LoginRequiredMixin, TeamleaderRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/upload.html"
    success_url = reverse_lazy("documents:index")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class DocumentUpdateView(LoginRequiredMixin, TeamleaderRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/edit.html"
    success_url = reverse_lazy("documents:index")


class DocumentDeleteView(LoginRequiredMixin, TeamleaderRequiredMixin, DeleteView):
    model = Document
    template_name = "documents/delete_confirm.html"
    success_url = reverse_lazy("documents:index")
