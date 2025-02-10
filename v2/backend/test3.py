from flask import Flask, request, jsonify
import sqlite3
import json  

app = Flask(__name__)

# Database paths
ADMIN_DB_PATH = "contest.db"      
USER_DB_PATH = "bookstore.db"      

def get_admin_db_connection():
    conn = sqlite3.connect(ADMIN_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_db_connection():
    conn = sqlite3.connect(USER_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Predefined correct queries (for `bookstore` schema)
CORRECT_ANSWERS = {
    1: "SELECT * FROM books WHERE price > 20;",  # Books with price > 20
    2: "SELECT COUNT(*) FROM customers;",  # Number of customers
    3: "SELECT name FROM authors WHERE country = 'United Kingdom';",  # UK authors
    4: "SELECT title FROM books WHERE genre = 'Fantasy';",  # Fantasy books
    5: "SELECT SUM(total_price) FROM orders;",  # Total revenue
    6: "SELECT title FROM books ORDER BY price DESC LIMIT 1;",  # Most expensive book
    7: "SELECT AVG(price) FROM books;",  # Average book price
    8: "SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders);",  # Customers who placed orders
    9: "SELECT title FROM books WHERE stock < 50;",  # Books with stock < 50
    10: "SELECT COUNT(DISTINCT genre) FROM books;"  # Number of unique genres
}

@app.route('/submit_query', methods=['POST'])
def submit_query():
    data = request.json
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    user_query = data.get('query', '')
    
    # Disallow modification queries
    if any(word in user_query.upper() for word in ["DROP", "DELETE", "INSERT", "UPDATE"]):
        return jsonify({"error": "Modifications are not allowed!"})
    
    try:
        # 1. Check if the user already submitted an answer for this question
        admin_conn = get_admin_db_connection()
        admin_cursor = admin_conn.cursor()
        admin_cursor.execute("SELECT * FROM submissions WHERE user_id = ? AND question_id = ?", 
                             (user_id, question_id))
        existing_submission = admin_cursor.fetchone()
        if existing_submission:
            admin_conn.close()
            return jsonify({"error": "You have already submitted an answer for this question."})
        admin_conn.close()
        
        # 2. Execute user's query on `bookstore` database
        user_conn = get_user_db_connection()
        user_cursor = user_conn.cursor()
        user_cursor.execute(user_query)
        user_results = user_cursor.fetchall()
        user_data = [dict(row) for row in user_results]
        user_conn.close()
        
        # 3. Execute the correct query on `bookstore` database
        correct_query = CORRECT_ANSWERS.get(question_id)
        if not correct_query:
            return jsonify({"error": "Correct query not defined for this question."})
        
        correct_conn = get_user_db_connection()  # Run correct query on the same `bookstore` DB
        correct_cursor = correct_conn.cursor()
        correct_cursor.execute(correct_query)
        correct_results = correct_cursor.fetchall()
        correct_data = [dict(row) for row in correct_results]
        correct_conn.close()
        
        # 4. Compare results (ignoring row order)
        sorted_user = sorted(user_data, key=lambda x: json.dumps(x, sort_keys=True))
        sorted_correct = sorted(correct_data, key=lambda x: json.dumps(x, sort_keys=True))
        is_correct = 1 if sorted_user == sorted_correct else 0
        
        # 5. Store the submission in `admin_db.sqlite`
        admin_conn = get_admin_db_connection()
        admin_cursor = admin_conn.cursor()
        admin_cursor.execute(
            "INSERT INTO submissions (user_id, question_id, user_query, is_correct) VALUES (?, ?, ?, ?)",
            (user_id, question_id, user_query, is_correct)
        )
        admin_conn.commit()
        admin_conn.close()
        
        return jsonify({"message": "Answer submitted!", "correct": is_correct})
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/finish', methods=['POST'])
def finalize_score():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        conn = get_admin_db_connection()
        cursor = conn.cursor()

        # Check if user already has a final score
        cursor.execute("SELECT * FROM final_scores WHERE user_id = ?", (user_id,))
        existing_record = cursor.fetchone()

        if existing_record:
            conn.close()
            return jsonify({"error": "Score already finalized for this user"}), 400

        # Calculate total score from submissions
        cursor.execute("SELECT SUM(is_correct) as total_score FROM submissions WHERE user_id = ?", (user_id,))
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
        conn = get_admin_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, score FROM final_scores ORDER BY score DESC LIMIT 2")
        winner = cursor.fetchall()
        conn.close()
        return jsonify({"winners": [dict(row) for row in winner]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
