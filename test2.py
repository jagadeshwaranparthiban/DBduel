from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('contest_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# Predefined correct answers for each question
CORRECT_ANSWERS = {
    1: "SELECT * FROM participants WHERE score > 80;",
    2: "SELECT MAX(score) FROM participants;",
    3: "SELECT * FROM participants ORDER BY score DESC;",
    4: "SELECT COUNT(*) FROM participants;",
    5: "SELECT * FROM participants WHERE name LIKE 'A%';",
    6: "SELECT score FROM participants ORDER BY score DESC LIMIT 1 OFFSET 1;",
    7: "SELECT * FROM participants WHERE score = (SELECT MIN(score) FROM participants);",
    8: "SELECT COUNT(DISTINCT score) FROM participants;",
    9: "SELECT * FROM participants WHERE score >= 90;",
    10: "SELECT AVG(score) FROM participants;"
}

# Create tables if not exist
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        question_id INTEGER NOT NULL,
        user_query TEXT NOT NULL,
        is_correct INTEGER NOT NULL DEFAULT 0,
        UNIQUE(user_id, question_id) -- Prevent multiple submissions per question
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        user_id TEXT PRIMARY KEY,
        total_score INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

setup_database()

# Route to submit queries (only once per question)
@app.route('/submit_query', methods=['POST'])
def submit_query():
    data = request.json
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    user_query = data.get('query', '')

    if any(word in user_query.upper() for word in ["DROP", "DELETE", "INSERT", "UPDATE"]):
        return jsonify({"error": "Modifications are not allowed!"})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user has already submitted for this question
        cursor.execute("SELECT * FROM submissions WHERE user_id = ? AND question_id = ?", (user_id, question_id))
        existing_submission = cursor.fetchone()

        if existing_submission:
            conn.close()
            return jsonify({"error": "You have already submitted an answer for this question."})

        # Check correctness
        is_correct = int(user_query.strip().upper() == CORRECT_ANSWERS[question_id].strip().upper())

        # Store submission
        cursor.execute("INSERT INTO submissions (user_id, question_id, user_query, is_correct) VALUES (?, ?, ?, ?)",
                       (user_id, question_id, user_query, is_correct))

        conn.commit()
        conn.close()

        return jsonify({"message": "Answer submitted!", "correct": is_correct})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to view output of a query
@app.route('/view_output', methods=['POST'])
def view_output():
    data = request.json
    user_query = data.get('query', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(user_query)
        results = cursor.fetchall()
        conn.close()

        return jsonify({"results": [dict(row) for row in results]})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to finish contest and calculate final score
@app.route('/finish', methods=['POST'])
def finish_contest():
    data = request.json
    user_id = data.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Calculate total score
    cursor.execute("SELECT SUM(is_correct) FROM submissions WHERE user_id = ?", (user_id,))
    total_score = cursor.fetchone()[0] or 0

    # Store final score
    cursor.execute("INSERT INTO scores (user_id, total_score) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET total_score = ?",
                   (user_id, total_score, total_score))

    conn.commit()
    conn.close()

    return jsonify({"message": "Contest completed!", "total_score": total_score})

if __name__ == '__main__':
    app.run(debug=True)
