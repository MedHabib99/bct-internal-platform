# feedback/urls.py
from django.urls import path
from . import views

app_name = "feedback"

urlpatterns = [
    # seller-facing
    path("", views.index, name="index"), 
    path("my/", views.my_list, name="my_list"),
    path("new/", views.create, name="new"),
    path("thanks/", views.thanks, name="thanks"),
    path("<int:pk>/", views.detail, name="detail"),

    # teamleader actions
    path("admin/", views.admin_list, name="admin_list"),
    path("<int:pk>/reply/", views.admin_reply, name="admin_reply"),
    path("<int:pk>/status/", views.admin_set_status, name="admin_set_status"),
]
