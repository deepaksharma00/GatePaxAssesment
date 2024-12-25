import os
import pymysql
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables from .env file
# load_dotenv("/app/.env")

# Cloud SQL configuration
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")  # Public IP or via Cloud SQL Auth Proxy

# Secret key for validation
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")


@app.route("/", methods=["POST"])
def handle_transaction():
    # Validate secret key
    secret_key = request.headers.get("secret_key")
    if secret_key != SECRET_KEY:
        return jsonify({"error": f"Unauthorized {secret_key} != {SECRET_KEY}"}), 401

    # Validate account_id query parameter
    account_id = request.args.get("account_id")
    if not account_id:
        return jsonify({"error": "Missing required query parameter: account_id"}), 400

    # Validate JSON body
    try:
        data = request.get_json()
        transaction_id = data.get("transaction_id")
        description = data.get("description")
        amount = data.get("amount")

        if not transaction_id or not description or amount is None:
            return jsonify({"error": "Missing required JSON fields"}), 400

    except Exception as e:
        return jsonify({"error": f"Invalid JSON body: {str(e)}"}), 400

    # Insert into Cloud SQL database
    try:
        # connection = pymysql.connect(
        #     host=DB_HOST,
        #     user=DB_USER,
        #     password=DB_PASSWORD,
        #     database=DB_NAME,
        #     cursorclass=pymysql.cursors.DictCursor,
        # )
        connection = pymysql.connect(
        unix_socket=DB_HOST,  # Use the Cloud SQL Unix socket
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=10
        )
        with connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO transactions (transaction_id, account_id, description, amount)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (transaction_id, account_id, description, amount))
            connection.commit()

        return jsonify({"message": "Transaction added successfully"}), 201

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


def handler(request):
    return app(request.environ, start_response=lambda *args: None)