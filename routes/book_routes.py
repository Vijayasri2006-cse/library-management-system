import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for

# Create the Blueprint
book_bp = Blueprint('book_bp', __name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="Lms_#@8389",  # Your MySQL password
        database="library_db"  # Your database name
    )

# Route for adding a book
@book_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        authors = request.form['authors']
        genre = request.form['genre']
        total_copies = request.form['total_copies']
        shelf_number = request.form['shelf_number']
        publisher = request.form['publisher']
        branch = request.form['branch']
        year = request.form['year']

        try:
            # Connect to database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert the book details into the database
            cursor.execute("""
                INSERT INTO books (title, authors, genre, total_copies, shelf_number, publisher, branch, year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, authors, genre, total_copies, shelf_number, publisher, branch, year))

            # Commit the transaction
            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for('book_bp.view_books'))  # Redirect to the 'View Books' page after insertion

        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('add_books.html')  # Display the form for adding a book

# Route to view all books
@book_bp.route('/view_books')
def view_books():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('view_books.html', books=books)  # Pass books to the template

    except mysql.connector.Error as err:
        return f"Error: {err}"