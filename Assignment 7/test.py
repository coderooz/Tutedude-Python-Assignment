# Assignment 7/test.py

from db_config import connect

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            marks INTEGER
        );
    """)
    conn.commit()
    conn.close()
    print("Table created successfully.")

def insert_student(name, marks):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, marks) VALUES (%s, %s)", (name, marks))
    conn.commit()
    conn.close()
    print(f"Inserted: {name}, {marks}.")

def get_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students;")
    rows = cur.fetchall()
    conn.close()
    print("Student Records:")
    for row in rows:
        print(row)

def update_student(id, name, marks):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=%s, marks=%s WHERE id=%s", (name, marks, id))
    conn.commit()
    conn.close()
    print(f"Updated ID {id}.")

def delete_student(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    print(f"Deleted ID {id}.")

# Demo/Test Script
if __name__ == "__main__":
    create_table()
    insert_student("Alice", 85)
    insert_student("Bob", 70)
    get_students()
    update_student(1, "Alice Smith", 90)
    delete_student(2)
    get_students()