# Flask Library Management System - Project Files

## Complete Project Structure

```
library-management-flask/
├── README.md
├── app.py
├── requirements.txt
├── run.py
├── templates/
│   ├── add_book.html
│   ├── add_member.html
│   ├── base.html
│   ├── books.html
│   ├── index.html
│   ├── issue_book.html
│   ├── members.html
│   ├── transactions.html
```

## File Descriptions

### Core Application Files
- **app.py** - Main Flask application with all routes and database logic
- **requirements.txt** - Python package dependencies
- **run.py** - Alternative script to start the application
- **README.md** - Comprehensive documentation and setup instructions

### Templates (HTML Files)
- **templates/base.html** - Base template with navigation and layout
- **templates/index.html** - Dashboard with statistics and recent activity
- **templates/books.html** - Display all books in the library
- **templates/add_book.html** - Form to add new books
- **templates/members.html** - Display all library members
- **templates/add_member.html** - Form to register new members
- **templates/issue_book.html** - Form to issue books to members
- **templates/transactions.html** - View all borrowing transactions

### Database (Created on First Run)
- **library.db** - SQLite database file (auto-created)

## How to Use

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python app.py
   # OR
   python run.py
   ```

3. **Access the Application:**
   Open your browser and go to: http://127.0.0.1:5000

## Key Features Implemented

✅ **Modern Web Interface**: Bootstrap 5 responsive design
✅ **Database Integration**: SQLite with proper schema
✅ **Form Validation**: Flask-WTF with server-side validation  
✅ **CRUD Operations**: Create, Read, Update, Delete for all entities
✅ **Transaction Management**: Issue and return books with due dates
✅ **Fine Calculation**: Automatic overdue fine calculation
✅ **Dashboard**: Statistics and recent activity overview
✅ **Navigation**: Clean sidebar navigation between all sections
✅ **Flash Messages**: User feedback for all operations
✅ **Error Handling**: Proper error messages and validation

## Technical Stack

- **Backend**: Python 3.7+ with Flask framework
- **Database**: SQLite3 with relational schema
- **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome icons
- **Forms**: Flask-WTF and WTForms for validation
- **Templating**: Jinja2 template engine

This is a complete, ready-to-run Flask web application that converts the original command-line library management system into a modern web interface.
