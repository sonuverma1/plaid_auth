from django.urls import path, include
from .views import TokenExchange, FetchTransaction, Webhook, GetLinkToken, index

urlpatterns = [
    path('', index),
    path('tokenexchange/', TokenExchange.as_view()),
    path('fetchtrasaction/', FetchTransaction.as_view()),
    path('webhook/', Webhook.as_view()),
    path('linktoken/', GetLinkToken.as_view()),
]
