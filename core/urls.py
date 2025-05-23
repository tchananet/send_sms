from django.urls import path
from .views import receive_webhook
from .views import receive_webhook_recall
from .views import whatsapp_reminder_tomorrow, send_catalogue, send_whatsapp_ne_repond_pas
from .views import index

urlpatterns = [
    path("", index, name="home"),
    path("webhook/", receive_webhook, name="webhook"),
    path("send_whatsapp_recall/", receive_webhook_recall, name="webhook_recall"),
    path("send_whatsapp_reminder/", whatsapp_reminder_tomorrow, name="webhook_reminder"),
    path("send_catalogue/", send_catalogue, name="send_catalogue"),
    path("send_whatsapp_ne_repond_pas/", send_whatsapp_ne_repond_pas, name="send_whatsapp_no_answer"),
]