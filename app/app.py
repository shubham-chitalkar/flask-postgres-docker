import os
import time
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

# --------------------------------------------------
# Database Connection (Retry Safe)
# --------------------------------------------------
def get_db_connection():
    while True:
        try:
            return psycopg2.connect(os.environ["DATABASE_URL"])
        except OperationalError as e:
            print(f"Database connection failed: {e}. Retrying...")
            time.sleep(2)

# --------------------------------------------------
# Create Tables on Startup
# --------------------------------------------------
def setup_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            birth_date DATE,
            email VARCHAR(100),
            enrolled_date DATE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------
@app.route("/")
def home():
    return "Flask API is running and connected to PostgreSQL 🚀"

# --------------------------------------------------
# Students APIs
# --------------------------------------------------
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO students (first_name, last_name, birth_date, email, enrolled_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING student_id;
        """, (
            data.get("first_name"),
            data.get("last_name"),
            data.get("birth_date"),
            data.get("email"),
            data.get("enrolled_date"),
        ))

        student_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "student_id": student_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(students), 200


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM students WHERE student_id = %s;",
        (student_id,)
    )
    student = cur.fetchone()

    cur.close()
    conn.close()

    if student:
        return jsonify(student), 200
    return jsonify({"message": "Student not found"}), 404

# --------------------------------------------------
# Items APIs
# --------------------------------------------------
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;",
        (name, description)
    )

    item_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": item_id,
        "name": name,
        "description": description
    }), 201


@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM items;")
    items = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(items), 200


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"message": "Item deleted successfully"}), 200

# --------------------------------------------------
# Application Start
# --------------------------------------------------
if __name__ == "__main__":
    # Flask running on HOST → use localhost
    os.environ.setdefault(
        "DATABASE_URL",
        "postgresql://admin:123456@localhost:5432/mydatabase"
    )

    setup_tables()
    app.run(host="0.0.0.0", port=5000, debug=True)
