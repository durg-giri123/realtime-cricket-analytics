"""
Database Connection and Session Manager for Cricbuzz LiveStats.
Provides thread-safe connections, automatic transaction management,
foreign key enforcement, and helper methods for querying with pandas.
"""

import os
import sqlite3
import pandas as pd
from typing import Generator, Any, Optional
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    os.getenv("DATABASE_PATH", "database/cricbuzz_stats.db")
)


def get_db_path() -> str:
    """Returns the absolute path to the SQLite database file."""
    db_path = os.getenv("DATABASE_PATH", DEFAULT_DB_PATH)
    if not os.path.isabs(db_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, db_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager providing a transactional database connection.
    Enforces foreign keys, enables WAL mode for concurrency,
    and automatically commits or rolls back on exception.
    """
    conn = sqlite3.connect(get_db_path())
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as exc:
        conn.rollback()
        raise exc
    finally:
        conn.close()


def initialize_database(schema_path: Optional[str] = None) -> bool:
    """
    Initializes the database using database/schema.sql.
    Creates all tables, constraints, and indexes.
    """
    if schema_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        schema_path = os.path.join(base_dir, "database", "schema.sql")

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_db_connection() as conn:
        conn.executescript(schema_sql)
    return True


def execute_query(sql: str, params: tuple = ()) -> pd.DataFrame:
    """
    Executes a read-only SQL query and returns the results as a pandas DataFrame.
    """
    with get_db_connection() as conn:
        df = pd.read_sql_query(sql, conn, params=params)
    return df


def execute_dml(sql: str, params: tuple = ()) -> int:
    """
    Executes an INSERT, UPDATE, or DELETE query and returns the last row ID
    or number of affected rows.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        last_id = cursor.lastrowid
        return last_id if last_id is not None else cursor.rowcount
