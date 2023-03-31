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
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                sample_date TEXT NOT NULL,
                location TEXT NOT NULL,
                min_temp REAL NOT NULL,
                max_temp REAL NOT NULL,
                avg_temp REAL NOT NULL
            );
        """)
        self.conn.commit() # Commits the changes to the database.

    def fetch_sample_data(self, location, start_date, end_date):
        """Fetches the sample data for a given location between two dates."""
        sql = f"""
            SELECT sample_date, min_temp, max_temp, avg_temp 
            FROM weather_data 
            WHERE location = ? 
            AND sample_date BETWEEN {start_date} AND {end_date} ?
        """
        self.cursor.execute(sql, (location, start_date, end_date))
        data = self.cursor.fetchall()
        return data
    
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
