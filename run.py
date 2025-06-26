#!/usr/bin/env python3
"""
Simple script to run the Flask Library Management System
"""

if __name__ == '__main__':
    from app import app, init_db

    # Initialize database on first run
    init_db()

    print("=" * 50)
    print("Flask Library Management System")
    print("=" * 50)
    print("Starting server...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)

    app.run(debug=True, host='127.0.0.1', port=5000)
