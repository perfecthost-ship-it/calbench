import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "calbench.db"

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        """Create database if missing."""
        if not self.db_path.exists():
            self._create_schema()

    def _create_schema(self):
        """Initialise database with CALBENCH schema."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.executescript("""
        CREATE TABLE instruments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial TEXT NOT NULL,
            model TEXT NOT NULL,
            range_min REAL,
            range_max REAL,
            resolution REAL,
            notes TEXT
        );

        CREATE TABLE certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrument_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            technician TEXT NOT NULL,
            environment_temp REAL,
            environment_humidity REAL,
            pass_fail TEXT,
            FOREIGN KEY (instrument_id) REFERENCES instruments(id)
        );

        CREATE TABLE readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id INTEGER NOT NULL,
            applied REAL NOT NULL,
            indicated REAL NOT NULL,
            error REAL NOT NULL,
            FOREIGN KEY (certificate_id) REFERENCES certificates(id)
        );

        CREATE TABLE equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            serial TEXT NOT NULL,
            expiry TEXT NOT NULL,
            uncertainty REAL NOT NULL
        );
        """)

        conn.commit()
        conn.close()

    # ---------------------------
    # Instrument operations
    # ---------------------------

    def add_instrument(self, serial, model, range_min, range_max, resolution, notes=""):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO instruments (serial, model, range_min, range_max, resolution, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (serial, model, range_min, range_max, resolution, notes))
        conn.commit()
        conn.close()

    def get_instrument(self, serial):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM instruments WHERE serial = ?", (serial,))
        row = cur.fetchone()
        conn.close()
        return row

    # ---------------------------
    # Certificate operations
    # ---------------------------

    def create_certificate(self, instrument_id, date, technician, temp, humidity, pass_fail):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO certificates (instrument_id, date, technician, environment_temp, environment_humidity, pass_fail)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (instrument_id, date, technician, temp, humidity, pass_fail))
        cert_id = cur.lastrowid
        conn.commit()
        conn.close()
        return cert_id

    def add_reading(self, certificate_id, applied, indicated):
        error = indicated - applied
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO readings (certificate_id, applied, indicated, error)
            VALUES (?, ?, ?, ?)
        """, (certificate_id, applied, indicated, error))
        conn.commit()
        conn.close()

    def get_certificate(self, cert_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM certificates WHERE id = ?", (cert_id,))
        cert = cur.fetchone()

        cur.execute("SELECT applied, indicated, error FROM readings WHERE certificate_id = ?", (cert_id,))
        readings = cur.fetchall()

        conn.close()
        return cert, readings

    # ---------------------------
    # Equipment operations
    # ---------------------------

    def get_equipment(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM equipment")
        rows = cur.fetchall()
        conn.close()
        return rows
