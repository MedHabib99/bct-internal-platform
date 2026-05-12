from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Contact
from django.urls import reverse_lazy
from .forms import ContactForm

def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__iexact="Teamleader").exists()
        )
    )

class ContactGridView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts/grid.html"
    context_object_name = "contacts"
    paginate_by = 24

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        qs = Contact.objects.all()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(title__icontains=q) |
                Q(email__icontains=q) |
                Q(whatsapp__icontains=q)
            )
        return qs.order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "").strip()
        ctx["is_teamleader"] = is_teamleader(self.request.user)
        return ctx

class TeamleaderRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not is_teamleader(request.user):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Teamleader access only.")
        return super().dispatch(request, *args, **kwargs)

class ContactCreateView(TeamleaderRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/form.html"
    success_url = reverse_lazy("contacts:index")

class ContactUpdateView(TeamleaderRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/form.html"
    success_url = reverse_lazy("contacts:index")

class ContactDeleteView(TeamleaderRequiredMixin, DeleteView):
    model = Contact
    template_name = "contacts/delete_confirm.html"
    success_url = reverse_lazy("contacts:index")