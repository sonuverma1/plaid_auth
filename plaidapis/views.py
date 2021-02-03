from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
from .models import Log, TokenItem, Transaction
from rest_framework.response import Response
from .tasks import get_account_and_item_metadata
from datetime import datetime, timedelta

from plaid import Client
# Create your views here.

client = Client(client_id=settings.PLAID_CLIENT_ID,
                secret=settings.PLAID_SECRET, environment=settings.PLAID_ENV)


class TokenExchange(APIView):
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
            TokenExchange.create(access_token=access_token,
                                 item_id=item_id, user=request.user)
            data = {'message': "Token exchange successfully"}
            get_account_and_item_metadata.delay(res)
            return Response(data, status=200)
        except Exception as e:
            data = {'message': str(e)}
            Log.objects.create(request=request.data, response=data)
            return Response(data, status=400)


class FetchTransaction(APIView):
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
