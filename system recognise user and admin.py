from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'cyberjaya_stray_scan_secret'

# 模拟数据库
users = {
    "admin@mmu.edu.my": {
        "password": generate_password_hash("admin123"),
        "role": "admin"
    },
    "student@mmu.edu.my": {
        "password": generate_password_hash("user123"),
        "role": "user"
    }
}

# --- 登录页面展示 ---
@app.route('/')
def login_page():
    return render_template('login.html')

# --- 登录逻辑处理 ---
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user_data = users.get(email)

    if user_data and check_password_hash(user_data['password'], password):
        session['user'] = email
        session['role'] = user_data['role']
        
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    else:
        flash("Email or Password incorrect!")
        return redirect(url_for('login_page'))

# --- 管理员后台 ---
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("Access Denied: Admins Only!")
        return redirect(url_for('login_page'))
    return "<h1>Admin Portal</h1><p>Welcome, Boss. You can manage all stray reports here.</p>"

# --- 普通用户后台 ---
@app.route('/user/home')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return f"<h1>User Home</h1><p>Welcome {session['user']}! Report a stray animal here.</p>"

if __name__ == '__main__':
    app.run(debug=True)