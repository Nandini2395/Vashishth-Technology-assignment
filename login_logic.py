import sqlite3

# Create a connection to the SQLite database
connection = sqlite3.connect("database.db")

# Create a cursor object
cursor = connection.cursor()

# Create the 'students' table (if not already created)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        month_name TEXT, 
        student_name TEXT, 
        present_days INTEGER, 
        absent_days INTEGER
    )
""")

# Define the list of students
student_list = [
    ("January", "Raj Modi", 20, 2),
    ("January", "Arnav Khanna", 22, 0)
]

# Insert data into the 'students' table
cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", student_list)

# Create the 'professors' table (for login functionality)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS professors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
""")

# Define the list of professors (sample data)
professor_list = [
    ("Udyan Chatterjee", "Udyan@123"),
    ("Neelam Kathoria", "Neelam@123"),  # Added the missing comma here
    ("Nandini Sharma", "Nandini@123")
]

# Insert data into the 'professors' table
for professor in professor_list:
    try:
        cursor.execute("INSERT INTO professors (username, password) VALUES (?, ?)", professor)
    except sqlite3.IntegrityError:
        # Ignore if the professor already exists
        pass

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database created and data inserted successfully!")