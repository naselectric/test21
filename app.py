from flask import Flask, render_template, request
import psycopg2
from psycopg2 import sql, OperationalError

app = Flask(__name__)

# Database connection settings
# DB_HOST = "cacfu3mcmfvpcb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
# DB_NAME = "da8dtnf0egi6bk"
# DB_USER = "u5uprh4r9pbe7b"
# DB_PASS = "pf84168705fee3d216f4c65c59785287a9f482002b2f22b363d38157174246a2f"

def create_connection():
    """Create and return a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return None
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    # Input validation
    if not name or not email:
        return "Invalid input. Please fill all fields.", 400

    conn = create_connection()
    if conn is None:
        return "Database connection error.", 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("INSERT INTO users (name, email) VALUES (%s, %s)"),
                (name, email)
            )
        conn.commit()
        return "Data saved successfully!"
    except Exception as e:
        conn.rollback()
        return f"Error saving data: {e}", 500
    finally:
        conn.close()
if __name__ == '__main__':
    app.run(debug=True)
