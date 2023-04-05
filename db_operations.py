"""
This module adds functionality to the Weather App but managing database data
that is parsed from the scrape_weather module.
"""
from datetime import datetime
from datetime import timedelta
from pprint import pprint
import re
import sqlite3
from dbcm import DBCM
from scrape_weather import WeatherDataParser

class DBOperations:
    def __init__(self):
        """
        This constructor creates a connection and cursor for the database.
        """
        self.conn = sqlite3.connect("weather_database.sqlite")
        self.cursor = self.conn.cursor()
        print("Opened database successfully.")

    def initialize_db(self):
        """
        Initializes the weather_data table in the database with the necessary columns.
        """

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

    def save_data(self, data):
        """
        Saves weather data to the database for each date in the given dictionary.
        """

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
                            INSERT INTO weather_data 
                            (sample_date, 
                            location,
                            max_temp, 
                            min_temp, 
                            mean_temp)
                            VALUES (?, ?, ?, ?, ?)
                        """, (sample_date,
                              location,
                              max_temp,
                              min_temp,
                              mean_temp))
                        self.conn.commit()
                        print(f"Data saved for {sample_date}")
                    except sqlite3.Error as e:
                        print(f"Error inserting data for {sample_date}: {e}")
        print('Data saved to the database.')

    def purge_data(self):
        """
        Deletes all data from the weather_data table in the database.
        """
        self.cursor.execute('DELETE FROM weather_data')
        self.conn.commit()
        print('All data purged from the database.')

    def close(self):
        """
        Closes the database connection.
        """

        self.cursor.close()
        self.conn.close()

    def fetch_data(self, start_date, end_date):
        """
        This method fetches the data from the database according to what the 
        user inputs for the start and end dates.
        """

        # Convert start and end dates to the correct format for the database
        start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d')

        # Create an empty list to store the temperature data for each date
        data = []

        # Loop through the dates and fetch the temperature data for each date
        while start_date_formatted <= end_date_formatted:
            sample_date = start_date_formatted.strftime('%B %d, %Y')
            # Drop leading zeroes only from the day portion of the formatted date
            sample_date = re.sub(r'(?<=\s)0', '', sample_date)
            self.cursor.execute("""
                SELECT max_temp, min_temp, mean_temp 
                FROM weather_data 
                WHERE sample_date = ?
            """, (sample_date,))
            result = self.cursor.fetchone()

            # If the temperature data for the date exists, add it to the list
            if result:
                max_temp, min_temp, mean_temp = result
                data.append((sample_date, max_temp, min_temp, mean_temp))

            # Increment the date by one day
            start_date_formatted += timedelta(days=1)

        # Return the list of temperature data as a tuple
        return tuple(data)

def create_entire_database():
    """
    This function creates the database for the first time in order to retrieve data.
    """
    # Create a WeatherDataParser object to get the weather data
    parser = WeatherDataParser()

    # Create a DBOperations object to save the weather data to the database
    db = DBOperations()
    db.initialize_db()
    db.save_data(parser.get_weather_dictionary())
    db.close()

if __name__ == "__main__":
    """
    This is the main function that instantiates a db object, and has
    functionality to parse initial data to the database. 
    """

    # create_entire_database()

    # Create a DBOperations object to fetch weather data from the database
    db = DBOperations()

    # Prompt the user for start and end dates
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    # Fetch data from the database for the specified date range
    data = db.fetch_data(start_date, end_date)

    # Output data to the screen in the form of a tuple
    pprint(data)

    # Close the database connection
    db.close()
       