from django.urls import path
from .views import receive_webhook

urlpatterns = [
    path("webhook/", receive_webhook, name="webhook"),
]