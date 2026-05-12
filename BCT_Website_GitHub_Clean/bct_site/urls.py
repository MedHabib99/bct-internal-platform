from django.contrib import admin
from django.urls import path, include
from .views import home, logout_view
from django.conf import settings
from django.conf.urls.static import static
from .views import home, logout_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("documents/", include(("documents.urls", "documents"), namespace="documents")),
    path("contacts/", include(("contacts.urls", "contacts"), namespace="contacts")),
    path("feedback/", include(("feedback.urls", "feedback"), namespace="feedback")),
    path("work-safety/", include(("worksafety.urls", "worksafety"), namespace="worksafety")),
    path("general-info/", include(("generalinfo.urls", "generalinfo"), namespace="generalinfo")),
    path("partners/", include(("partners.urls", "partners"), namespace="partners")),
    path("news/", include(("news.urls", "news"), namespace="news")),
    path("events/", include(("events.urls", "events"), namespace="events")),
    path("signout/", logout_view, name="signout"),
    path("", home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
