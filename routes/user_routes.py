from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.config import db# Ensure your database is correctly imported
# Define Blueprint
users_bp= Blueprint('users', __name__)
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        roll_number = request.form['roll_number']
        email = request.form['email']
        password = request.form['password']
        contact_number = request.form['contact_number']
        branch = request.form['branch']
        year = request.form['year']

        # Insert user details into MySQL database
        cursor = db.cursor()
        sql = """INSERT INTO users (username, roll_number, email, password, contact_number, branch, year)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (username, roll_number, email, password, contact_number, branch, year)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

        flash("Registration successful! Please login.", "success")

        # ✅ Redirect to User Login Page
        return redirect(url_for('users.user_login'))

    return render_template('user-register.html')  # Ensure this matches your register form template
    @user_bp.route('/login',methods=['GET','POST'])
    def login():
        return 
        render_template('user_login.html')