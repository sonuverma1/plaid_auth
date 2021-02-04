# plaid_auth
##Objective
Create a project in django rest framework and celery with following APIs exposed:
1) User signup, login , logout APIs
2) Token exchange API : An authenticated user can submit a plaid public token that
he gets post link integration.
a) This public token is exchanged for access token on the backend.b) This initiates an async job on the backend for fetching account and item
metadata for the access token.
3) Expose a webhook for handling plaid transaction updates and fetch the
transactions on receival of a webhook.
4) Expose an api endpoint for fetching all transaction and account data each for a
user.
5) Do appropriate plaid error handling


##Models
![Models](https://i.ibb.co/m6ybhSx/models.png)
