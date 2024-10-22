from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  
jwt = JWTManager(app)

def generateToken(email):
    access_token = create_access_token(identity=email)
    return access_token

if __name__ == "__main__":
    userEmail = "user@Kingsmanraju.com"  
    token = generateToken(userEmail)
    print("Generated JWT Token:", token)
