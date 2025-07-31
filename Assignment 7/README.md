# Assignment 7 - Student Management System

This repository contains is a comprehensive student management system built with Python, Tkinter, and PostgreSQL for managing student information and grades, as part of **Module 12: Building Database Apps with PostgreSQL & Python**.

## Features

### Student Management
- Add new students with name, email, class, and phone
- Update existing student information
- Delete students (with cascade deletion of grades)
- View all students in a sortable table
- Input validation for required fields

### Grade Management
- Add grades for students by subject
- Update existing grades
- Delete grades
- Support for custom maximum marks
- Automatic percentage calculation
- View all grades with student information

### Search and Filter
- Search students by name (case-insensitive)
- Filter students by class
- Filter grades by subject
- Reset all filters to show complete data
- Combined view of students and their grades

### Database Features
- PostgreSQL database with proper relationships
- Foreign key constraints with cascade deletion
- Data validation and error handling
- Sample data for testing

## Prerequisites

- Python 3.7 or higher
- PostgreSQL database server
- Required Python packages (see requirements.txt)

## Installation

1. **Install PostgreSQL**
   - Download and install PostgreSQL from https://www.postgresql.org/
   - Create a database named "testDb"
   - Set up a user "postgres" with password "1234" (or modify db_config.py)

2. **Install Python Dependencies**
   ```bash
   pip install psycopg2-binary
   or 
   pip install psycopg2
   ```

3. **Database Setup**
   - Ensure your PostgreSQL server is running
   - Run the test script:
   ```bash
   python test.py
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## Project Structure

```
student_management_system/
├── main.py                 # Main application file
├── db_config.py           # Database configuration
├── Assignment 7.pdf       # Assignment Text
└── README.md             # This file
```

## Database Schema

### Students Table
- `id`: Primary key (Serial)
- `name`: Student name (VARCHAR 100, NOT NULL)
- `email`: Student email (VARCHAR 100, UNIQUE, NOT NULL)
- `class_name`: Student class (VARCHAR 50, NOT NULL)
- `phone`: Phone number (VARCHAR 20)
- `created_at`: Timestamp (DEFAULT CURRENT_TIMESTAMP)

### Grades Table
- `id`: Primary key (Serial)
- `student_id`: Foreign key to students table
- `subject`: Subject name (VARCHAR 100, NOT NULL)
- `grade`: Grade obtained (DECIMAL 5,2, NOT NULL)
- `max_marks`: Maximum marks (DECIMAL 5,2, DEFAULT 100)
- `exam_date`: Date of exam (DATE)
- `created_at`: Timestamp (DEFAULT CURRENT_TIMESTAMP)

## Usage Instructions

### Adding Students
1. Go to the "Students" tab
2. Fill in the required fields (Name, Email, Class)
3. Phone number is optional
4. Click "Add Student"

### Managing Grades
1. Go to the "Grades" tab
2. Select a student from the dropdown
3. Enter subject, grade, and maximum marks
4. Click "Add Grade"

### Searching and Filtering
1. Go to the "Search & Filter" tab
2. Use any of the search options:
   - Search by student name
   - Filter by class
   - Filter by subject
3. Click "Reset All" to clear filters

### Updating Records
1. Select a record in any table
2. The form fields will auto-populate
3. Modify the desired fields
4. Click "Update Student" or "Update Grade"

### Deleting Records
1. Select a record in any table
2. Click "Delete Student" or "Delete Grade"
3. Confirm the deletion in the popup dialog

## Configuration

To modify database connection settings, edit `db_config.py`:

```python
def connect():
    return psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
```

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid input data
- Duplicate email addresses
- Missing required fields
- Database constraint violations


## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in db_config.py
   - Verify database "testDb" exists

2. **Module Not Found Error**
   - Install required packages
   - Ensure Python 3.7+ is installed

3. **Permission Denied**
   - Check PostgreSQL user permissions
   - Ensure user has CREATE, INSERT, UPDATE, DELETE privileges

4. **Tkinter Not Found**
   - On Linux: `sudo apt-get install python3-tk`
   - On macOS: Usually included with Python
   - On Windows: Included with Python installer



## 📘 Reference

This assignment is based on:

* **Module 10**: Introduction to GUI using Tkinter
* **Module 11**: Building GUI Projects
* **Module 12**: Building Database Apps with PostgreSQL & Python

---

## 🧪 Testing

* ✅ Performs `CURD` operations with search functions.
* ✅ UI buttons work as expected with responsive layout.

---
