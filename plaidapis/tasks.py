from celery import shared_task
from plaid import Client
from django.conf import settings
from .models import Account, Item, Transaction
# Create your views here.

client = Client(client_id=settings.PLAID_CLIENT_ID,
                secret=settings.PLAID_SECRET, environment=settings.PLAID_ENV)


@shared_task
def get_account_and_item_metadata(request_data):
    access_token = request_data['access_token']
    try:
        response1 = client.Accounts.get(access_token)
        accounts = response1['accounts']

        response2 = client.Item.get(access_token)
        item = response2['item']
        status = response2['status']
        data = {"account_get_response": response1,
                "item_get_response": response2}
        Account.objects.create(data=response1)
        Item.objects.create(data=response2)
    except Exception as e:
        data = {"message": str(e)}
    Log.objects.create(request=request_data, response=data)
