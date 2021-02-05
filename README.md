# plaid_auth
## Objective
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



## Models

![Models](https://i.ibb.co/m6ybhSx/models.png)


User: To store user login info

TokenIten: To store Access_token and Item_id info

Log: To store every activity log

Transactions: To store transactions info from Plaid API

Items: To store info of each Items

Account: To store bank account info

## REST APIs

### auth/registration/: 
To register a user

### auth/login:
To login a user

### auth/logout:
To logout already logged-in user

### api/linktoken:
-> To get link_token for logged-in user

### api/tokenexchange:
->exchange public_token to get access_token

### api/fetchtrasaction:
-> Fetch transaction of loggedIn user

### api/webhook:
-> Exposed webhook api for handling plaid transactions
### api/:
-> Link account and go in to plaid auth flow

## How to use
step 1) Create a config.py file in plaid_auth directory and create a Setting object having plaid credentials as its properties

step 2) Install all the required dependecies from requirements.txt

step 3) Run the program and goto signup/login api to create/login your account

step 4) Go to api/ url to start the plaid auth flow for getting access token for one item

step 5) Goto fetchtransaction/url to fetch all the transactions between a start time and time
