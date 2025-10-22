from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = 'my-secret-key-123'

# إعداد نظام تسجيل الدخول
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# نموذج مستخدم مبسط (دون قاعدة بيانات حقيقية)
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# تخزين المستخدمين في الذاكرة فقط
users = {
    'admin': User(1, 'admin')
}
passwords = {
    'admin': 'password123'
}
next_user_id = 2

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('home.html')

# صفحة التسجيل
@app.route('/register', methods=['GET', 'POST'])
def register():
    global next_user_id
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('يرجى إدخال كل المعلومات', 'error')
            return render_template('register.html')
        if username in users:
            flash('اسم المستخدم مسجّل مسبقاً', 'error')
            return render_template('register.html')
        user = User(next_user_id, username)
        users[username] = user
        passwords[username] = password
        next_user_id += 1
        flash('تم إنشاء الحساب! يمكنك تسجيل الدخول الآن', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and passwords.get(username) == password:
            user = users[username]
            login_user(user)
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    return render_template('login.html')

# لوحة التحكم
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# تسجيل الخروج
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
