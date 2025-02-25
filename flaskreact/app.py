from flask import Flask,jsonify,request
from flask_bcrypt import Bcrypt 
app = Flask(__name__)
bcrypt = Bcrypt(app)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/register', methods=['POST'])
def register():
    # รับค่าจาก request body (JSON)
    data = request.get_json()

    # ดึงค่าจาก JSON
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    password = data.get('password')
    # ตรวจสอบว่ามีค่าครบหรือไม่
    if not all([first_name, last_name, username, password]):
        return jsonify({"error": "Missing fields"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # จำลองการบันทึกข้อมูล (ในกรณีจริงต้องใช้ฐานข้อมูล)
    user_data = {
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "password": hashed_password    # ควรเข้ารหัสก่อนบันทึก (bcrypt)
    }

    return jsonify({"message": "User registered successfully", "user": user_data}), 201

if __name__ == '__main__':
    app.run(debug=True)