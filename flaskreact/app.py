from flask import Flask,jsonify,request
from flask_cors import CORS  
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Thanyawit@localhost:3306/user'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Run this once to create the database
with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/register', methods=['POST'])
def register():
    #  request body (JSON)
    data = request.get_json()

    # Json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    password = data.get('password')
    # validate data
    if not all([first_name, last_name, username, password]):
        return jsonify({"error": "Missing fields"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Map Model to data Json
    user_data = User(
        first_name= data['firstName'],
        last_name= data['lastName'],
        username= data['username'],
        password= hashed_password    # hash (bcrypt)
    )
    db.session.add(user_data)  # Add new user to the session
    db.session.commit()  # Save to the databas

    #Convert User object to a dictionary before returning
    user_data = {
        "id": user_data.id,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "username": user_data.username
    }

    return jsonify({"message": "User registered successfully", "user": user_data}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()

    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", 
                    "user": {
                        "firstName": user.first_name,
                        "lastName": user.last_name
                             }
                    }), 200



if __name__ == '__main__':
    app.run(debug=True)