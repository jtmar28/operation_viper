# start of DBOperations.py file
import sqlite3
from scrape_weather import WeatherDataParser
from datetime import datetime
from pprint import pprint

class DBOperations:
    def __init__(self):
        self.conn = sqlite3.connect("weather_database.sqlite")
        self.cursor = self.conn.cursor()
        print("Opened database successfully.") 

    def initialize_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                sample_date TEXT,
                location TEXT,
                max_temp REAL,
                min_temp REAL,                
                mean_temp REAL
            );
        """) 
        self.conn.commit()

# sample weather dictionary - {“2018-06-01”: {“max_temp”: 12.0, “min_temp”: 5.6, “mean_temp”: 7.1}, “2018-06-02”: {“max_temp”: 12.0, “min_temp”: 5.6, “mean_temp”: 7.1}}

    def save_data(self, data):
        for sample_date, temps in data.items():
            location = 'Winnipeg'
            max_temp = temps.get('max_temp', None)
            min_temp = temps.get('min_temp', None)          
            mean_temp = temps.get('mean_temp', None)
            if max_temp is not None and min_temp is not None and mean_temp is not None:
                self.cursor.execute("""
                    SELECT * 
                    FROM weather_data 
                    WHERE sample_date=?
                """, (sample_date,))
                existing_data = self.cursor.fetchone()
                if existing_data:
                    print(f"Data already exists for {sample_date}. Skipping...")
                else:
                    try:
                        self.cursor.execute("""
                            INSERT INTO weather_data (sample_date, location, max_temp, min_temp, mean_temp)
                            VALUES (?, ?, ?, ?, ?)
                        """, (sample_date, location, max_temp, min_temp, mean_temp))
                        self.conn.commit()
                        print(f"Data saved for {sample_date}")
                    except sqlite3.Error as e:
                        print(f"Error inserting data for {sample_date}: {e}")
        print('Data saved to the database.')

    def purge_data(self):
        self.cursor.execute('DELETE FROM weather_data')
        self.conn.commit()
        print('All data purged from the database.')

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def fetch_data(self, start_date, end_date):
        # Convert start and end dates to the correct format for the database
        start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B %d, %Y')
        end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B %d, %Y')

        # Execute the query using the formatted dates
        self.cursor.execute("""
            SELECT sample_date, max_temp, min_temp, mean_temp 
            FROM weather_data 
            WHERE sample_date >= ? AND sample_date <= ?
        """, (start_date_formatted, end_date_formatted))

        # Return the fetched data
        return self.cursor.fetchall()

def create_entire_database():
    # Create a WeatherDataParser object to get the weather data
    parser = WeatherDataParser()
    # Create a DBOperations object to save the weather data to the database
    db = DBOperations()
    db.initialize_db()
    db.save_data(parser.get_weather_dictionary())
    db.close()

if __name__ == "__main__":

    # create_entire_database()

    # Create a DBOperations object to fetch weather data from the database
    db = DBOperations()

    # Prompt the user for start and end dates
    # start_date = input("Enter start date (YYYY-MM-DD): ")
    # end_date = input("Enter end date (YYYY-MM-DD): ")

    # Fetch data from the database for the specified date range
    # data = db.fetch_data(start_date, end_date)
    data = db.fetch_data("2023-03-01", "2023-03-10")

    # Output data to the screen in the form of a tuple
    pprint(tuple(data))

    # Close the database connection
    db.close() 
 
# end of DBOperations.py 
       
