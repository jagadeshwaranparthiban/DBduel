import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('contest_db.sqlite')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a sample table (e.g., a table for storing participants and their scores)
cursor.execute('''
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    score INTEGER NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    correct_query TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,  
    question_id INTEGER NOT NULL,
    user_query TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS final_scores (
    user_id TEXT PRIMARY KEY,
    score INTEGER NOT NULL
)
''')

# Insert some sample data
cursor.execute("INSERT INTO participants (name, score) VALUES ('Alice', 85)")
cursor.execute("INSERT INTO participants (name, score) VALUES ('Bob', 90)")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database 'contest_db.sqlite' and table 'participants' created successfully!")
