from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "contest_db.sqlite"  # Path to your SQLite database

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return results as dictionary
    return conn

@app.route('/')
def home():
    return "SQLite Query Contest Server Running!"



@app.route('/query', methods=['POST'])
def execute_query():
    data = request.json
    user_query = data.get('query', '')
    user_id = data.get('user_id', '')  # Assume a user ID is passed
    question_id = data.get('question_id', '')  # The ID of the question being answered

    if not user_query or not user_id or not question_id:
        return jsonify({"error": "Missing required fields: query, user_id, or question_id"})

    # Prevent modification queries
    if any(keyword in user_query.upper() for keyword in ["DROP", "DELETE", "INSERT", "UPDATE"]):
        return jsonify({"error": "Modifications are not allowed!"})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the correct query for the given question
        cursor.execute("SELECT correct_query FROM questions WHERE id = ?", (question_id,))
        question = cursor.fetchone()

        if not question:
            conn.close()
            return jsonify({"error": "Invalid question ID"})

        correct_query = question["correct_query"]

        # Execute user's query
        cursor.execute(user_query)
        user_result = cursor.fetchall()

        # Execute correct query
        cursor.execute(correct_query)
        correct_result = cursor.fetchall()

        # Compare results and award points
        score = 1 if user_result == correct_result else 0

        # Save submission
        cursor.execute(
            "INSERT INTO submissions (user_id, question_id, user_query, score) VALUES (?, ?, ?, ?)",
            (user_id, question_id, user_query, score)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Query submitted successfully!",
            "score_awarded": score
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    
#final score calculation
@app.route('/finish', methods=['POST'])
def finalize_score():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already has a final score
        cursor.execute("SELECT * FROM final_scores WHERE user_id = ?", (user_id,))
        existing_record = cursor.fetchone()

        if existing_record:
            conn.close()
            return jsonify({"error": "Score already finalized for this user"}), 400

        # Calculate total score from submissions
        cursor.execute("SELECT SUM(score) as total_score FROM submissions WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        total_score = result["total_score"] if result["total_score"] is not None else 0

        # Store the final score in the final_scores table
        cursor.execute("INSERT INTO final_scores (user_id, score) VALUES (?, ?)", (user_id, total_score))
        conn.commit()
        conn.close()

        return jsonify({"message": "Final score saved successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/winners', methods=['GET'])
def winners():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, score FROM final_scores ORDER BY score DESC LIMIT 2")
        winner = cursor.fetchall()
        conn.close()
        return jsonify({"winners": winner})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
