#!/usr/bin/env python3
"""
Demo script for Flask Library Management System
This script demonstrates the database functionality without running the web server.
"""

import sqlite3
import os
from datetime import datetime, timedelta

def create_demo_data():
    """Create some sample data for demonstration"""

    # Remove existing database for fresh start
    if os.path.exists('library.db'):
        os.remove('library.db')
        print("🗑️  Removed existing database")

    # Connect to database
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create tables
    print("📊 Creating database tables...")

    cursor.execute("""
        CREATE TABLE books (
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

    cursor.execute("""
        CREATE TABLE members (
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

    cursor.execute("""
        CREATE TABLE transactions (
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

    # Insert sample books
    print("📚 Adding sample books...")
    sample_books = [
        ("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4", "fiction", 3, 2020),
        ("1984", "George Orwell", "978-0-452-28423-4", "fiction", 2, 1949),
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5", "fiction", 2, 1925),
        ("Python Programming", "John Smith", "978-1-23456-789-0", "technology", 5, 2023),
        ("Data Structures", "Jane Doe", "978-0-98765-432-1", "science", 3, 2022),
        ("World History", "Robert Brown", "978-0-11111-222-3", "history", 2, 2021)
    ]

    for title, author, isbn, category, copies, year in sample_books:
        cursor.execute("""
            INSERT INTO books (title, author, isbn, category, total_copies, available_copies, publication_year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, author, isbn, category, copies, copies, year))

    # Insert sample members
    print("👥 Adding sample members...")
    sample_members = [
        ("Alice Johnson", "alice@email.com", "555-0101", "123 Main St", "student"),
        ("Bob Wilson", "bob@email.com", "555-0102", "456 Oak Ave", "faculty"),
        ("Carol Davis", "carol@email.com", "555-0103", "789 Pine Rd", "staff"),
        ("David Miller", "david@email.com", "555-0104", "321 Elm St", "public")
    ]

    for name, email, phone, address, member_type in sample_members:
        cursor.execute("""
            INSERT INTO members (name, email, phone, address, member_type)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, address, member_type))

    # Insert sample transactions
    print("📝 Adding sample transactions...")
    today = datetime.now().date()

    # Current loans
    cursor.execute("""
        INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
        VALUES (1, 1, ?, ?, 'issued')
    """, (today - timedelta(days=5), today + timedelta(days=9)))

    cursor.execute("""
        INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
        VALUES (2, 2, ?, ?, 'issued')
    """, (today - timedelta(days=10), today + timedelta(days=4)))

    # Update available copies for issued books
    cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id IN (1, 2)")

    # Past returned transaction
    cursor.execute("""
        INSERT INTO transactions (book_id, member_id, issue_date, due_date, return_date, status, fine_amount)
        VALUES (3, 3, ?, ?, ?, 'returned', 0.00)
    """, (today - timedelta(days=20), today - timedelta(days=6), today - timedelta(days=3)))

    conn.commit()
    conn.close()

    print("✅ Demo database created successfully!")
    print("📊 Database contents:")

    # Show summary
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    book_count = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    member_count = cursor.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    transaction_count = cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    print(f"   📚 Books: {book_count}")
    print(f"   👥 Members: {member_count}")
    print(f"   📝 Transactions: {transaction_count}")

    # Show current issued books
    issued = cursor.execute("""
        SELECT b.title, m.name, t.due_date
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN members m ON t.member_id = m.id
        WHERE t.status = 'issued'
    """).fetchall()

    print(f"\n📖 Currently issued books:")
    for book in issued:
        print(f"   • '{book[0]}' to {book[1]} (due: {book[2]})")

    conn.close()

if __name__ == '__main__':
    print("🚀 Flask Library Management System - Demo Setup")
    print("=" * 50)
    create_demo_data()
    print("\n🎉 Demo data setup complete!")
    print("\n💡 Now you can run the Flask app:")
    print("   python app.py")
    print("\n🌐 Then visit: http://127.0.0.1:5000")
    print("   The web interface will show the demo data.")
