from flask import Flask, request, jsonify, send_file, abort
from database import addUser, getUserByEmail, getUserById, addExpenseToDB, getUserExpenses, getAllExpenses, init_db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
import csv
import os

init_db()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'a9d656d0b4554ebdaa59590a4bf50ad1907cca5b55f47a909984ddc624f6def4'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email or not password:
            return jsonify({"msg": "Email and password are required"}), 400

        user = getUserByEmail(email)
        if user and user['password'] == password:
            accessToken = create_access_token(identity=user['email'])
            return jsonify(accessToken=accessToken, userId=user['id']), 200
        return jsonify({"msg": "Bad email or password"}), 401
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@app.route('/users', methods=['POST'])
def createUser():
    try:
        data = request.json
        if not data.get('name') or not data.get('email') or not data.get('mobile') or not data.get('password'):
            return jsonify({"msg": "All fields (name, email, mobile, password) are required"}), 400

        addUser(data['name'], data['email'], data['mobile'], data['password'])
        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def getUser(user_id):
    try:
        user = getUserById(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"msg": "User not found"}), 404
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@app.route('/expenses', methods=['POST'])
@jwt_required()
def addExpense():
    try:
        userEmail = get_jwt_identity()
        data = request.json

        if not data.get('description') or not data.get('amount') or not data.get('split_type') or not data.get('participants'):
            return jsonify({"msg": "All fields (description, amount, split_type, participants) are required"}), 400

        if data['split_type'] == 'equal':
            slitData = json.dumps({
                "equal_split": data['amount'] / len(data['participants'])
            })
        elif data['split_type'] == 'exact':
            slitData = json.dumps(data.get('exact_splits', {}))
        elif data['split_type'] == 'percentage':
            if sum(data.get('percentages', {}).values()) != 100:
                return jsonify({"msg": "Percentages must add up to 100"}), 400
            slitData = json.dumps(data['percentages'])
        else:
            return jsonify({"msg": "Invalid split type"}), 400

        addExpenseToDB(userEmail, data['description'], data['amount'], data['split_type'], slitData)
        return jsonify({"msg": "Expense added successfully"}), 201
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@app.route('/expenses/<int:user_id>', methods=['GET'])
@jwt_required()
def getUserExpense(user_id):
    try:
        expenses = getUserExpenses(user_id)
        if expenses:
            return jsonify(expenses), 200
        return jsonify({"msg": "No expenses found for this user"}), 404
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@app.route('/expenses', methods=['GET'])
@jwt_required()
def getAllExpense():
    try:
        expenses = getAllExpenses()
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@app.route('/balance-sheet/download/<int:user_id>', methods=['GET'])
@jwt_required()
def downloadBalanceSheet(user_id):
    try:
        expenses = getUserExpenses(user_id)
        if not expenses:
            return jsonify({"msg": "No expenses found for this user"}), 404

        csv_file = f'balance_sheet_{user_id}.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Expense ID", "Description", "Amount", "Split Type", "Split Data", "Created At"])
            for exp in expenses:
                writer.writerow([exp['id'], exp['description'], exp['amount'], exp['split_type'], exp['split_data'], exp['created_at']])

        return send_file(csv_file, as_attachment=True)
    except Exception as e:
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
