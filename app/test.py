import unittest
from main import create_app, db  # Assuming your Flask app is in 'app.py'
from flask_jwt_extended import create_access_token
import json

class TestDailyExpensesApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')  # Assuming there's a config for testing
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()  # Create the database schema

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()  # Drop the database after tests

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "mobile": "1234567890",
            "password": "password123"
        }
        self.expense_data = {
            "description": "Dinner",
            "amount": 3000,
            "split_type": "equal",
            "participants": ["user1@example.com", "user2@example.com"]
        }

    def test_01_create_user(self):
        """Test user creation endpoint"""
        response = self.client.post('/create_user', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], "User created successfully")

    def test_02_login_user(self):
        """Test user login and receive JWT token"""
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data)
        self.jwt_token = response_data['access_token']  # Save JWT for future requests

    def test_03_add_expense(self):
        """Test adding an expense with JWT token"""
        self.test_02_login_user()  # Ensure JWT token is available
        headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Content-Type': 'application/json'
        }
        response = self.client.post('/expenses', data=json.dumps(self.expense_data), headers=headers)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], "Expense added successfully")

    def test_04_retrieve_user_expenses(self):
        """Test retrieving individual user expenses"""
        self.test_02_login_user()  # Ensure JWT token is available
        headers = {
            'Authorization': f'Bearer {self.jwt_token}'
        }
        response = self.client.get('/expenses/user/testuser@example.com', headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('expenses', response_data)

    def test_05_retrieve_overall_expenses(self):
        """Test retrieving overall expenses for all users"""
        self.test_02_login_user()  # Ensure JWT token is available
        headers = {
            'Authorization': f'Bearer {self.jwt_token}'
        }
        response = self.client.get('/expenses/overall', headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('total_expenses', response_data)

    def test_06_download_balance_sheet(self):
        """Test downloading the balance sheet"""
        self.test_02_login_user()  # Ensure JWT token is available
        headers = {
            'Authorization': f'Bearer {self.jwt_token}'
        }
        response = self.client.get('/expenses/balance_sheet', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/octet-stream')  # For file download

if __name__ == '__main__':
    unittest.main()
