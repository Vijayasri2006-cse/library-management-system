import mysql.connector

# ✅ Create MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",    # Replace with your MySQL username
    password="Lms_#@8389",  # Replace with your MySQL password
    database="library_db"   # Replace with your MySQL database name
)