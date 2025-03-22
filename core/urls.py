from django.urls import path
from .views import receive_webhook
from .views import receive_webhook_recall

urlpatterns = [
    path("webhook/", receive_webhook, name="webhook"),
    path("send_whatsapp_recall/", receive_webhook_recall, name="webhook"),
]