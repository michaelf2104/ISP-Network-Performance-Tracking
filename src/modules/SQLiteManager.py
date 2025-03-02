from ast import List
import sqlite3
import logging

class SQLiteManager:
    """
    Manages SQLite database operations.
    """

    def __init__(self, db_path: str):
        """
        Initialize the SQLite database.

        @param db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_database()

    def update_last_processed(self, measurement_id: str, timestamp: int):
        """
        Updates the last processed timestamp for a measurement.

        @param measurement_id: The measurement ID
        @param timestamp: The new last processed timestamp
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO last_processed (measurement_id, last_timestamp)
                    VALUES (?, ?);
                """, (measurement_id, timestamp))
                conn.commit()
                logging.info(f"Updated last processed timestamp for measurement {measurement_id}: {timestamp}")
        except Exception as e:
            logging.error(f"Error updating last processed for {measurement_id}: {e}")


    def _initialize_database(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS measurements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        measurement_id TEXT UNIQUE,
                        asn TEXT,
                        bucket_name TEXT,
                        retention_policy TEXT,
                        interval INTEGER,
                        measurement_type TEXT
                    );
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS last_processed (
                        measurement_id TEXT PRIMARY KEY,
                        last_timestamp INTEGER
                    );
                """)
                conn.commit()
            logging.info("Database initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing database: {e}")

    def add_measurement(self, measurement_id: str, asn: str, bucket_name: str, retention_policy: str, interval: int, measurement_type: str):
        """
        Add a new measurement to the database.

        @param measurement_id: Measurement ID
        @param asn: ASN number
        @param bucket_name: InfluxDB bucket name
        @param retention_policy: Data retention policy
        @param interval: Measurement interval in seconds
        @param measurement_type: Type of measurement (Ping, Traceroute, etc.)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO measurements (measurement_id, asn, bucket_name, retention_policy, interval, measurement_type)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (measurement_id, asn, bucket_name, retention_policy, interval, measurement_type))
                conn.commit()
                logging.info(f"Measurement {measurement_id} added to database.")
        except Exception as e:
            logging.error(f"Error adding measurement {measurement_id}: {e}")

    def get_measurements(self) -> List:
        """
        Retrieve all measurements from the database.

        @return: List of measurement records
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM measurements;")
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching measurements: {e}")
            return []

    def get_last_processed(self, measurement_id: str) -> int:
        """
        Get the last processed timestamp for a given measurement.

        @param measurement_id: Measurement ID
        @return: Last processed timestamp or 0 if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT last_timestamp FROM last_processed WHERE measurement_id = ?;", (measurement_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logging.error(f"Error fetching last processed timestamp for {measurement_id}: {e}")
            return 0
