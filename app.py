from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

DATABASE = 'library.db'

# Database helper functions
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(DATABASE)
        g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db = get_db()

        # Create books table
        db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                category TEXT NOT NULL,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                publication_year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create members table
        db.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                member_type TEXT DEFAULT 'student',
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)

        # Create transactions table
        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                issue_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                status TEXT DEFAULT 'issued',
                fine_amount DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (member_id) REFERENCES members (id)
            )
        """)

        db.commit()
        print("Database initialized successfully!")

# WTForms classes
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(min=1, max=100)])
    isbn = StringField('ISBN', validators=[Length(min=0, max=20)])
    category = SelectField('Category', choices=[
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('reference', 'Reference')
    ], validators=[DataRequired()])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    publication_year = IntegerField('Publication Year', validators=[NumberRange(min=1900, max=2024)])
    submit = SubmitField('Add Book')

class MemberForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=100)])
    phone = StringField('Phone', validators=[Length(min=0, max=15)])
    address = TextAreaField('Address')
    member_type = SelectField('Member Type', choices=[
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('public', 'Public')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Member')

class IssueBookForm(FlaskForm):
    book_id = SelectField('Book', coerce=int, validators=[DataRequired()])
    member_id = SelectField('Member', coerce=int, validators=[DataRequired()])
    issue_date = DateField('Issue Date', default=datetime.now().date(), validators=[DataRequired()])
    submit = SubmitField('Issue Book')

# Routes
@app.route('/')
def index():
    db = get_db()

    # Get statistics
    total_books = db.execute('SELECT COUNT(*) as count FROM books').fetchone()['count']
    total_members = db.execute('SELECT COUNT(*) as count FROM members WHERE is_active = 1').fetchone()['count']
    issued_books = db.execute('SELECT COUNT(*) as count FROM transactions WHERE status = "issued"').fetchone()['count']
    overdue_books = db.execute("""
        SELECT COUNT(*) as count FROM transactions 
        WHERE status = "issued" AND due_date < date("now")
    """).fetchone()['count']

    # Recent transactions
    recent_transactions = db.execute("""
        SELECT t.*, b.title, m.name as member_name
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN members m ON t.member_id = m.id
        ORDER BY t.created_at DESC
        LIMIT 5
    """).fetchall()

    return render_template('index.html', 
                         total_books=total_books,
                         total_members=total_members,
                         issued_books=issued_books,
                         overdue_books=overdue_books,
                         recent_transactions=recent_transactions)

@app.route('/books')
def books():
    db = get_db()
    books = db.execute('SELECT * FROM books ORDER BY title').fetchall()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        db = get_db()
        try:
            db.execute("""
                INSERT INTO books (title, author, isbn, category, total_copies, available_copies, publication_year)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (form.title.data, form.author.data, form.isbn.data, 
                  form.category.data, form.total_copies.data, form.total_copies.data, form.publication_year.data))
            db.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('books'))
        except sqlite3.IntegrityError:
            flash('Error: ISBN already exists!', 'error')

    return render_template('add_book.html', form=form)

@app.route('/members')
def members():
    db = get_db()
    members = db.execute('SELECT * FROM members WHERE is_active = 1 ORDER BY name').fetchall()
    return render_template('members.html', members=members)

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        db = get_db()
        try:
            db.execute("""
                INSERT INTO members (name, email, phone, address, member_type)
                VALUES (?, ?, ?, ?, ?)
            """, (form.name.data, form.email.data, form.phone.data, form.address.data, form.member_type.data))
            db.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('members'))
        except sqlite3.IntegrityError:
            flash('Error: Email already exists!', 'error')

    return render_template('add_member.html', form=form)

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    db = get_db()
    form = IssueBookForm()

    # Populate choices for books and members
    available_books = db.execute('SELECT id, title, author FROM books WHERE available_copies > 0').fetchall()
    active_members = db.execute('SELECT id, name FROM members WHERE is_active = 1').fetchall()

    form.book_id.choices = [(book['id'], f"{book['title']} by {book['author']}") for book in available_books]
    form.member_id.choices = [(member['id'], member['name']) for member in active_members]

    if form.validate_on_submit():
        due_date = form.issue_date.data + timedelta(days=14)  # 2 weeks loan period

        # Insert transaction
        db.execute("""
            INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'issued')
        """, (form.book_id.data, form.member_id.data, form.issue_date.data, due_date))

        # Update available copies
        db.execute("""
            UPDATE books SET available_copies = available_copies - 1 
            WHERE id = ?
        """, (form.book_id.data,))

        db.commit()
        flash('Book issued successfully!', 'success')
        return redirect(url_for('transactions'))

    return render_template('issue_book.html', form=form)

@app.route('/transactions')
def transactions():
    db = get_db()
    transactions = db.execute("""
        SELECT t.*, b.title, b.author, m.name as member_name
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN members m ON t.member_id = m.id
        ORDER BY t.created_at DESC
    """).fetchall()

    current_date = datetime.now().date().strftime('%Y-%m-%d')
    return render_template('transactions.html', transactions=transactions, current_date=current_date)

@app.route('/return_book/<int:transaction_id>')
def return_book(transaction_id):
    db = get_db()

    # Get transaction details
    transaction = db.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,)).fetchone()

    if transaction and transaction['status'] == 'issued':
        return_date = datetime.now().date()

        # Calculate fine if overdue
        due_date = datetime.strptime(transaction['due_date'], '%Y-%m-%d').date()
        fine_amount = 0.0
        if return_date > due_date:
            overdue_days = (return_date - due_date).days
            fine_amount = overdue_days * 2.0  # $2 per day fine

        # Update transaction
        db.execute("""
            UPDATE transactions 
            SET return_date = ?, status = 'returned', fine_amount = ?
            WHERE id = ?
        """, (return_date, fine_amount, transaction_id))

        # Update available copies
        db.execute("""
            UPDATE books SET available_copies = available_copies + 1 
            WHERE id = ?
        """, (transaction['book_id'],))

        db.commit()

        if fine_amount > 0:
            flash(f'Book returned successfully! Fine: ${fine_amount:.2f}', 'warning')
        else:
            flash('Book returned successfully!', 'success')
    else:
        flash('Invalid transaction or book already returned!', 'error')

    return redirect(url_for('transactions'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
