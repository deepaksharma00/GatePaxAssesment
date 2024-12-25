import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# Read database connection details from environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")

# SQL to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255),
    description TEXT,
    amount DECIMAL(10, 2)
);
"""

try:
    # Create a connection to the database
    engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    # Connect to the database
    with engine.connect() as connection:
        print("Successfully connected to the database.")

        # Execute the SQL to create the table
        connection.execute(text(create_table_sql))
        print("Table `transactions` created successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
