from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
from .models import Log, TokenItem, Transaction
from rest_framework.response import Response
from .tasks import get_account_and_item_metadata
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated

from plaid import Client
# Create your views here.

client = Client(client_id=settings.PLAID_CLIENT_ID,
                secret=settings.PLAID_SECRET, environment='sandbox')


def index(request):
    return render(request, 'index.html', context={})


class GetLinkToken(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            configs = {
                'user': {
                    'client_user_id': '123-test-user-id',
                },
                'products': ['auth', 'transactions'],
                'client_name': "Plaid Test App",
                'country_codes': ['US'],
                'language': 'en',
                'webhook': 'http://localost:8000/api/webhook',  # endpoint to my webhook
                'link_customization_name': 'default',
                'account_filters': {
                    'depository': {
                        'account_subtypes': ['checking', 'savings'],
                    },
                },

            }
            response = client.LinkToken.create(configs)
            link_token = response['link_token']
            data = {'link_token': link_token}
            return Response(data, status=200)
        except Exception as e:
            data = {"message": str(e)}
            return Response(data, status=400)


class TokenExchange(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            public_token = request.data['public_token']
            response = client.Item.public_token.exchange(public_token)
            access_token = response['access_token']
            item_id = response['item_id']
            request_id = response['request_id']
            req = {'public_token': request.data['public_token']}
            res = {'access_token': access_token,
                   'item_id': item_id, "request_id": request_id}
            Log.objects.create(request=req, response=res)
            TokenItem.objects.create(access_token=access_token,
                                     item_id=item_id, user=request.user)
            data = {'message': "Token exchange successfully"}
            get_account_and_item_metadata.delay(res)
            return Response(data, status=200)
        except Exception as e:
            data = {'message': str(e)}
            Log.objects.create(request=request.data, response=data)
            return Response(data, status=400)


class FetchTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            start_date = request.data['start_date']
            end_date = request.data['end_date']
            tokenitem = TokenItem.objects.get(user=request.user)
            access_token = tokenitem.access_token
            response = client.Transactions.get(access_token,
                                               start_date=start_date,
                                               end_date=end_date)
            transactions = response['transactions']
            # Manipulate the count and offset parameters to paginate
            # transactions and retrieve all available data
            while len(transactions) < response['total_transactions']:
                response = client.Transactions.get(access_token,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   offset=len(transactions)
                                                   )
                transactions.extend(response['transactions'])
            data = {"transactions": transactions}
            Transaction.objects.create(data=data)
            status_code = 200
        except Exception as e:
            data = {"message": str(e)}
            status_code = 400
        Log.objects.create(request=request.data, response=data)
        return Response(data, status=status_code)


class Webhook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            item_id = request.data['item_id']
            tokenitem = TokenItem.objects.get(item_id=item_id)
            access_token = tokenitem.access_token
            response = client.Transactions.get(access_token,
                                               start_date=datetime.now -
                                               timedelta(days=30),
                                               end_date=datetime.now)
            transactions = response['transactions']
            data = {"transactions": transactions}
            Transaction.objects.create(data=data)
            status_code = 200
        except Exception as e:
            data = {"message": str(e)}
            status_code = 400
        Log.objects.create(request=request.data, response=data)
        return Response(status_code=status_code)
