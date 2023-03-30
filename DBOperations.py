import sqlite3

class DBOperations:
    def __init__(self, weather_database):
        """Called when object is created. Initializes databaase connection and cursor."""
        self.weather_database = weather_database # assigns weather_database argument to self.weather_database attribute of DBOperations instance.
        self.conn = sqlite3.connect(weather_database) # creates a connection to weather_database.
        self.cursor = self.conn.cursor() # creates a cursor object.

    def __del__(self):
        """Called when the object is about to be destroyed."""
        self.cursor.close()
        self.conn.close()

    def initialize_db(self):
        """Creates the weather_data table if it does not already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_date TEXT,
                location TEXT,
                min_temp REAL,
                max_temp REAL,
                avg_temp REAL
            )
        """)
        self.conn.commit() # Commits the changes to the database.

    def fetch_data(self, location, sample_date):
        """Takes location and sample_date parameters to return the desired data from the database."""
        self.cursor.execute('SELECT min_temp, max_temp, avg_temp FROM weather_data WHERE location = ? AND sample_date = ?', (location, sample_date))
        data = self.cursor.fetchall()

    def save_data(self, sample_date, location, min_temp, max_temp, avg_temp):
        """Inserts and commits data to the weather_data table if it does not already exist."""
        sql = """
                  INSERT OR IGNORE INTO weather_data (sample_date, location, min_temp, max_temp, avg_temp)
                  VALUES (?, ?, ?, ?, ?);
              """
        data = (sample_date, location, min_temp, max_temp, avg_temp)
        self.cursor.execute(sql, data)
        self.conn.commit()

    def purge_data(self):
        """Deletes all data from the weather_data table."""
        self.cursor.execute('DELETE FROM weather_data')
        self.conn.commit()
