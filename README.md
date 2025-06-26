# Flask Library Management System

A simple yet comprehensive web-based Library Management System built with Flask, SQLite, and Bootstrap.

## Features

- **Dashboard**: Overview of library statistics and recent activities
- **Book Management**: Add, view, and manage book inventory
- **Member Management**: Register and manage library members
- **Book Circulation**: Issue and return books with due date tracking
- **Transaction History**: Complete record of all library transactions
- **Fine Calculation**: Automatic overdue fine calculation
- **Responsive Design**: Modern Bootstrap UI that works on all devices

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Forms**: Flask-WTF and WTForms
- **Icons**: Font Awesome

## Quick Start

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 2. Installation

```bash
# Clone or download the project
# Navigate to the project directory

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### 4. First Run Setup

On the first run, the application will automatically:
- Create the SQLite database (`library.db`)
- Set up all required tables (books, members, transactions)

## Usage Guide

### Dashboard
- View total books, members, issued books, and overdue items
- Monitor recent transactions

### Adding Books
1. Navigate to "Add Book" from the sidebar
2. Fill in book details (title, author, ISBN, category, etc.)
3. Specify number of copies
4. Submit the form

### Managing Members
1. Go to "Add Member" to register new members
2. Provide member details and select member type
3. View all members in the "Members" section

### Issuing Books
1. Click "Issue Book" from the sidebar
2. Select an available book and active member
3. Choose issue date (due date is automatically set to 14 days later)
4. Confirm the transaction

### Returning Books
1. Go to "Transactions" to see all book loans
2. Click "Return" button for issued books
3. System automatically calculates fines for overdue returns ($2/day)

## Database Schema

### Books Table
- id, title, author, isbn, category
- total_copies, available_copies, publication_year
- created_at timestamp

### Members Table  
- id, name, email, phone, address
- member_type, registration_date, is_active

### Transactions Table
- id, book_id, member_id
- issue_date, due_date, return_date
- status, fine_amount, created_at

## Configuration

### Secret Key
Change the SECRET_KEY in `app.py` for production:
```python
app.config['SECRET_KEY'] = 'your-unique-secret-key'
```

### Database Location
By default, the SQLite database is created as `library.db` in the project directory.

## Customization

### Adding New Book Categories
Edit the choices in the `BookForm` class in `app.py`:
```python
category = SelectField('Category', choices=[
    ('fiction', 'Fiction'),
    ('your-category', 'Your Category'),
    # Add more categories
])
```

### Changing Fine Rates
Modify the fine calculation in the `return_book` route:
```python
fine_amount = overdue_days * 2.0  # Change rate here
```

## File Structure

```
library-management-flask/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── library.db            # SQLite database (created on first run)
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Dashboard page
    ├── books.html        # Book listing
    ├── add_book.html     # Add book form
    ├── members.html      # Member listing
    ├── add_member.html   # Add member form
    ├── issue_book.html   # Issue book form
    └── transactions.html # Transaction history
```

## Contributing

This is a school project template. Feel free to:
- Add new features (search functionality, reports, etc.)
- Improve the UI/UX
- Add input validation
- Implement user authentication
- Add email notifications

## License

This project is created for educational purposes. Feel free to use and modify as needed.

## Support

For questions or issues, please refer to the Flask documentation:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
