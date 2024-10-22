# Daily Expenses Sharing Application

Here’s a README.md file for your project that explains how to set up, run, and test the API endpoints using curl:

Daily Expenses Sharing Application
This is a Flask-based API for managing user registration, login, expenses, and balance sheets. The API provides endpoints for user authentication and JWT-based authorization to secure user-specific operations like adding and retrieving expenses.

## Features
#### User Registration and Login with JWT-based authentication
#### Add and retrieve expenses
#### Split expenses equally, by percentage, or exact amounts
#### Download a balance sheet in CSV format
#### Secure API endpoints with JWT

## FILE SYSTEM

Here,
### app -- folder consists of database, auth, routes 
### check -- folder consists of checking module working conditions, generating the secret key
### test -- folder consists of testing curl script just for reference

## Installation

#### Clone Repository

```bash
git clone https://github.com/saiguptha2003/DailyExpensessharing_API.git
cd DailyExpensessharing_API
```

#### Create a virtual environment

```bash
python3 -m venv ExpenseCompiler
source ExpenseCompiler/bin/activate 
```

#### Install the required dependencies

```bash
pip install -r requirements.txt
```

#### Run Flask Server

```bash
cd app
python main.py
```
#### API is available in localhost 5000

```bash
http://127.0.0.1:5000

```

#### Generate secret-key
```bash
cd check
python generateSecretKey.py
```
#### Test Token Module
```bash
cd check
python tokenTest.py
```


## TESTING THE APPLICATION

### API ENDPOINTS

#### Register User

##### Endpoint: /users
##### Method: POST
##### Description: Register a new user.

```curl 
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{
  "name": "V D Panduranga Sai Guptha",
  "email": "saiguptha2003@gmail.com",
  "mobile": "8688670712",
  "password": "assessment"
}'
```

#### Login and JWT Generation

##### Endpoint: /login
##### Method: POST
##### Description: Log in with email and password to receive a JWT token.

```curl
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{
  "email": "saiguptha2003@gmail.com",
  "password": "assessment"
}'
```

#### Get User Details

##### Endpoint: /users/<userId>
##### Method: GET
##### Authentication: JWT token required.

```curl
curl -X GET http://127.0.0.1:5000/users/1 \
-H "Authorization: Bearer <your-jwt-token>"
```
replace your-jwt-token with the accessToken which present in response

#### Add an Expense

##### Endpoint: /expenses
##### Method: POST
##### Authentication: JWT token required.

```curl
curl -X POST http://127.0.0.1:5000/expenses \
-H "Authorization: Bearer <your-jwt-token>" \
-H "Content-Type: application/json" \
-d '{
  "description": "Dinner",
  "amount": 100,
  "split_type": "equal",
  "participants": ["user1", "user2"]
}'
```
replace your-jwt-token with the accessToken which present in response

#### Get User Expenses

##### Endpoint: /expenses/<user_id>
##### Method: GET
##### Authentication: JWT token required

```curl
curl -X GET http://127.0.0.1:5000/expenses/1 \
-H "Authorization: Bearer <your-jwt-token>"
```
replace your-jwt-token with the accessToken which present in response

#### Get All Expenses

##### Endpoint: /expenses
##### Method: GET
##### Authentication: JWT token required.

```curl
curl -X GET http://127.0.0.1:5000/expenses \
-H "Authorization: Bearer <your-jwt-token>"
```
replace your-jwt-token with the accessToken which present in response

#### Download Balance Sheet

##### Endpoint: /balance-sheet/download/<userId>
##### Method: GET
##### Authentication: JWT token required

```curl
curl -X GET http://127.0.0.1:5000/balance-sheet/download/1 \
-H "Authorization: Bearer <your-jwt-token>" \
--output balanceSheet1.csv

```

replace your-jwt-token with the accessToken which present in response