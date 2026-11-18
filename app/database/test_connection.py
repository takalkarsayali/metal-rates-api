
from sqlalchemy import text
from app.database.connection import engine


def test_connection():

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT version(), CURRENT_TIMESTAMP")
            )

            row = result.fetchone()

            print("Database connection successful!")
            print("PostgreSQL version:", row[0])
            print("Database time:", row[1])

    except Exception as e:

        print("Database connection failed!")
        print("Error:", e)


if __name__ == "__main__":
    test_connection()
