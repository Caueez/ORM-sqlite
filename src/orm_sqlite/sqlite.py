import sqlite3
from typing import Any


class SQLiteNotConnectedError(Exception):
    """Raised when an operation is attempted on a SQLite database without an established connection."""
    pass

class SQLiteQueryExecutionError(Exception):
    """Raised when an error occurs during the execution of a SQLite query."""
    pass


class SQLite:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def close(self):
        if not self.connection:
            raise SQLiteNotConnectedError("Database connection is not established.")

        self.connection.close()
        self.connection = None

    def execute_query(self, query : str, params : dict[str, Any] = {}) -> list[Any]:
        if not self.connection:
            raise SQLiteNotConnectedError("Database connection is not established.")
        
        cursor = self.connection.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            return cursor.fetchall()
        except SQLiteQueryExecutionError as e:
            raise SQLiteQueryExecutionError(f"Error occurred while executing query: {e}")

    def commit(self):
        if not self.connection:
            raise SQLiteNotConnectedError("Database connection is not established.")
        
        self.connection.commit()