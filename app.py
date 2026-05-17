from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="library_db"
    )


# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        roll_number = request.form.get('roll_number')
        email = request.form.get('email')
        password = request.form.get('password')
        contact_no = request.form.get('contact_no')
        course = request.form.get('course')
        year = request.form.get('year')

        db = get_db_connection()
        cursor = db.cursor()

        try:

            sql = """
            INSERT INTO users
            (username, roll_number, email, password, contact_no, course, year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                username,
                roll_number,
                email,
                password,
                contact_no,
                course,
                year
            )

            cursor.execute(sql, values)
            db.commit()

            flash("Registration Successful!", "success")

            return redirect(url_for('register'))

        except mysql.connector.Error as err:
            flash(f"Database Error: {err}", "danger")

        finally:
            cursor.close()
            db.close()

    return render_template('register.html')


# User Login
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            session['user_id'] = user['roll_number']
            session['username'] = user['username']

            return redirect(url_for('user_dashboard'))

        else:
            flash('Invalid username or password', 'danger')

    return render_template('user_login.html')


# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin123':
            return redirect(url_for('admin_dashboard'))

        else:
            return "<script>alert('Invalid credentials!'); window.location.href='/admin_login';</script>"

    return render_template('admin_login.html')


# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():

    if 'user_id' in session:
        return render_template(
            'user_dashboard.html',
            username=session['username']
        )

    else:
        flash("Please log in first.", "warning")
        return redirect(url_for('user_login'))


# Logout
@app.route('/logout')
def logout():

    session.clear()
    flash("Logged out successfully", "success")

    return redirect(url_for('index'))


# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        return render_template(
            'admin_dashboard.html',
            books=books
        )

    except Exception as e:
        return f"<h1>Error:</h1><p>{str(e)}</p>"

    finally:
        cursor.close()
        conn.close()


# View Users
@app.route('/view_users')
def view_users():

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT username, roll_number, email, password, contact_no, course, year FROM users"
        )

        users = cursor.fetchall()

        return render_template(
            'view_users.html',
            users=users
        )

    finally:
        cursor.close()
        conn.close()


# View Books
@app.route('/view_books', methods=['GET', 'POST'])
def view_books():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM books WHERE 1=1"
    values = []

    if request.method == 'POST':

        branch = request.form.get('branch')
        year = request.form.get('year')
        search_query = request.form.get('search_query')

        if branch and branch != 'All':
            query += " AND branch=%s"
            values.append(branch)

        if year and year != 'All':
            query += " AND year=%s"
            values.append(year)

        if search_query:
            query += " AND (title LIKE %s OR authors LIKE %s)"
            values.extend([
                f"%{search_query}%",
                f"%{search_query}%"
            ])

    cursor.execute(query, values)
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view_books.html', books=books)


# Add Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        book_id = request.form.get('book_id')
        title = request.form.get('title')
        authors = request.form.get('authors')
        genre = request.form.get('genre')
        total_copies = request.form.get('total_copies')
        shelf_number = request.form.get('shelf_number')
        publisher = request.form.get('publisher')
        branch = request.form.get('branch')
        year = request.form.get('year')

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO books
            (book_id, title, authors, genre, total_copies,
            shelf_number, publisher, branch, year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                book_id,
                title,
                authors,
                genre,
                total_copies,
                shelf_number,
                publisher,
                branch,
                year
            )

            cursor.execute(query, values)
            conn.commit()

            flash('Book added successfully!', 'success')

            return redirect(url_for('view_books'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_book'))

        finally:
            cursor.close()
            conn.close()

    return render_template('add_books.html')


# Update Book
@app.route('/update_book/<book_id>', methods=['GET', 'POST'])
def update_book(book_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        title = request.form['title']
        authors = request.form['authors']
        genre = request.form['genre']
        total_copies = request.form['total_copies']
        shelf_number = request.form['shelf_number']
        publisher = request.form['publisher']
        branch = request.form['branch']
        year = request.form['year']

        try:

            cursor.execute(
                '''
                UPDATE books
                SET title=%s,
                    authors=%s,
                    genre=%s,
                    total_copies=%s,
                    shelf_number=%s,
                    publisher=%s,
                    branch=%s,
                    year=%s
                WHERE book_id=%s
                ''',
                (
                    title,
                    authors,
                    genre,
                    total_copies,
                    shelf_number,
                    publisher,
                    branch,
                    year,
                    book_id
                )
            )

            conn.commit()

            flash('Book updated successfully!', 'success')

            return redirect(url_for('view_books'))

        except Exception as e:
            flash(f'Error updating book: {e}', 'danger')

        finally:
            cursor.close()
            conn.close()

    cursor.execute(
        'SELECT * FROM books WHERE book_id=%s',
        (book_id,)
    )

    book = cursor.fetchone()

    cursor.close()
    conn.close()

    if book:
        return render_template('update_books.html', book=book)

    else:
        flash('Book not found!', 'danger')
        return redirect(url_for('view_books'))


# Issued Books Page
@app.route('/issued_books')
def issued_books():
    return render_template('issued_books.html')


# API - Get Issued Books
@app.route('/api/issued_books')
def api_issued_books():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT issue_id,
                   book_id,
                   roll_number,
                   DATE_FORMAT(issue_date, '%Y-%m-%d') as issue_date,
                   DATE_FORMAT(due_date, '%Y-%m-%d') as due_date,
                   status
            FROM issued_books
            ORDER BY issue_date ASC
            """
        )

        books = cursor.fetchall()

        return jsonify(books)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# API - Issue Book
@app.route('/api/issue_book', methods=['POST'])
def api_issue_book():

    data = request.get_json()

    book_id = data.get('book_id')
    roll_number = data.get('roll_number')
    due_date = data.get('due_date')

    if not book_id or not roll_number or not due_date:
        return jsonify({
            "message": "All fields are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Check book

        cursor.execute(
            "SELECT * FROM books WHERE book_id=%s",
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            return jsonify({
                "message": "Book not found"
            }), 404

        # Check available copies

        available_copies = book['total_copies']

        if available_copies <= 0:
            return jsonify({
                "message": "No copies available"
            }), 400

        # Check user

        cursor.execute(
            "SELECT * FROM users WHERE roll_number=%s",
            (roll_number,)
        )

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "message": "Student not found"
            }), 404

        # Insert issued book

        cursor.execute(
            """
            INSERT INTO issued_books
            (book_id, roll_number, issue_date, due_date, status)
            VALUES (%s, %s, CURDATE(), %s, 'Issued')
            """,
            (book_id, roll_number, due_date)
        )

        # Reduce copies

        cursor.execute(
            """
            UPDATE books
            SET total_copies = total_copies - 1
            WHERE book_id = %s
            """,
            (book_id,)
        )

        conn.commit()

        return jsonify({
            "message": "Book issued successfully"
        })

    except Exception as e:

        conn.rollback()

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

# Borrowed Books
@app.route('/borrowed_books', methods=['GET', 'POST'])
def borrowed_books():

    # Check login

    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('user_login'))

    # Logged in user's roll number

    user_roll_number = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT ib.issue_id,
            ib.issue_date AS borrowed_date,
            ib.due_date,
            b.title,
            b.authors AS author
        FROM issued_books ib
        JOIN books b
            ON ib.book_id = b.book_id
        WHERE ib.roll_number = %s
        AND ib.status = 'Issued'
        ORDER BY ib.issue_date DESC
        """

        cursor.execute(query, (user_roll_number,))

        borrowed_books = cursor.fetchall()

        return render_template(
            'borrowed_books.html',
            borrowed_books=borrowed_books
        )

    except Exception as e:
        return f"<h3>Error fetching borrowed books: {e}</h3>"

    finally:
        cursor.close()
        conn.close()
 
@app.route('/return_books')
def return_books():

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('user_login'))

    user_roll_number = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT
            ib.issue_id,
            b.title AS book_title,
            b.authors AS author,
            ib.issue_date AS borrowed_date,
            ib.return_date AS returned_date
        FROM issued_books ib
        JOIN books b
        ON ib.book_id = b.book_id
        WHERE ib.roll_number = %s
        AND ib.status = 'Returned'
        ORDER BY ib.return_date DESC
        """

        cursor.execute(query, (user_roll_number,))

        return_books = cursor.fetchall()

        return render_template(
            'return_books.html',
            return_books=return_books
        )

    except Exception as e:
        return f"<h3>Error: {e}</h3>"

    finally:
        cursor.close()
        conn.close()
      
    


# Return Particular Book
@app.route('/return_book/<int:issue_id>')
def return_book(issue_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Get issued book details
        cursor.execute(
            """
            SELECT *
            FROM issued_books
            WHERE issue_id = %s
            """,
            (issue_id,)
        )

        issued_book = cursor.fetchone()

        # Check if book exists
        if not issued_book:

            flash("Book not found", "danger")

            return redirect(url_for('borrowed_books'))

        # Update status to Returned
        cursor.execute(
            """
            UPDATE issued_books
            SET
                status = 'Returned',
                return_date = CURDATE()
            WHERE issue_id = %s
            """,
            (issue_id,)
        )

        # Increase book copies
        cursor.execute(
            """
            UPDATE books
            SET total_copies = total_copies + 1
            WHERE book_id = %s
            """,
            (issued_book['book_id'],)
        )

        # Save changes
        conn.commit()

        flash("Book returned successfully", "success")

        return redirect(url_for('borrowed_books'))

    except Exception as e:

        conn.rollback()

        return f"<h3>Error: {e}</h3>"

    finally:

        cursor.close()
        conn.close()

# Reserve Book
@app.route('/reserve_book/<book_id>')
def reserve_book(book_id):

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('user_login'))

    roll_number = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # Check already reserved

        cursor.execute(
            """
            SELECT * FROM reserve_books
            WHERE book_id=%s
            AND roll_number=%s
            """,
            (book_id, roll_number)
        )

        existing = cursor.fetchone()

        if existing:

            flash("Book already reserved", "warning")

            return redirect(url_for('view_books'))

        # Insert reserve book

        cursor.execute(
            """
            INSERT INTO reserve_books
            (
                book_id,
                roll_number,
                reserve_date,
                pickup_deadline,
                status
            )

            VALUES
            (
                %s,
                %s,
                CURDATE(),
                NULL,
                'Waiting' 
            )
            """,
            (book_id, roll_number)
        )
        cursor.execute(
    """
    UPDATE reserve_books
    SET
        pickup_deadline = DATE_ADD(CURDATE(), INTERVAL 3 DAY),
        status = 'Ready for Pickup'

    WHERE book_id = %s
    AND status = 'Waiting'
    """,
    (book_id,)
)
        conn.commit()

        flash("Book reserved successfully", "success")

        return redirect(url_for('reserve_books'))

    except Exception as e:

        return f"<h3>Error: {e}</h3>"

    finally:

        cursor.close()
        conn.close()


# Reserve Books Page
@app.route('/reserve_books')
def reserve_books():

    # Check login
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('user_login'))

    roll_number = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT
            b.title AS book_title,
            b.authors AS author,
            rb.reserve_date,
            rb.pickup_deadline

        FROM reserve_books rb

        JOIN books b
        ON rb.book_id = b.book_id

        WHERE rb.roll_number = %s

        ORDER BY rb.reserve_date DESC
        """

        cursor.execute(query, (roll_number,))

        reserved_books = cursor.fetchall()

        return render_template(
            'reserve_books.html',
            reserved_books=reserved_books
        )

    except Exception as e:

        return f"<h3>Error: {e}</h3>"

    finally:

        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)

