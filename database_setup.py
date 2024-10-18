import sqlite3

# Connect to (or create) the database.db file
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop the 'users' table if you want to start fresh (use with caution)
cursor.execute("DROP TABLE IF EXISTS users")

# Create the 'users' table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'admin'))
)
''')

while True:
    input
    cursor.execute(f"""INSERT INTO users (username, password, role) VALUES ('user1', "{input()}", 'user')""")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin1', 'adminpass', 'admin')")
    # Create the 'videos' table to store video information (if it doesn't already exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        video_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        filename TEXT NOT NULL
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and tables created successfully!")
