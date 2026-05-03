from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# 🔥 الاتصال بـ RDS
connection = pymysql.connect(
    host='mysql -h mydb.ckrsaqqgq1yz.us-east-1.rds.amazonaws.com -P 3306 -u admin -p',   # ← حط endpoint هنا
    user='admin',
    password='#Almhlawi123',   # ← حط الباسورد
    database='attendance',
    cursorclass=pymysql.cursors.DictCursor
)

# 🟢 الصفحة الرئيسية
@app.route('/')
def index():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    students = cursor.fetchall()
    return render_template('index.html', students=students)


# ➕ إضافة طالب
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, status) VALUES (%s, %s)",
        (name, "Present")
    )
    connection.commit()

    return redirect('/')


# ✅ تحديث الحالة
@app.route('/update/<int:id>/<status>')
def update(id, status):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET status=%s WHERE id=%s",
        (status, id)
    )
    connection.commit()

    return redirect('/')


# ❌ حذف
@app.route('/delete/<int:id>')
def delete(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    connection.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)