##
#   Group Project:  Weather Processing App
#   Course:         ADEV-3005(234116)
#   Group:          #10
#   Team members:   Dean Lorenzo, Jesse Kosowan, Justin Martinez
#   Milestone:      #2
#   Updated:        Apr 8, 2023 
#

"""
This module adds functionality to the Weather App by managing database data
that is parsed from the scrape_weather module.
"""

from datetime import datetime, timedelta
from pprint import pprint
import re
import sqlite3
from dbcm import DBCM
from scrape_weather import WeatherDataParser

class DBOperations:
    def __init__(self):
        """
        Initializes an instance of the class with the following instance variables:
        - cursor: an instance of the DBCM class
        """

        self.cursor = DBCM("weather_database.sqlite")        
        print("Opened database successfully.")

    def initialize_db(self):
        """
        Initializes the weather_data table in the database with the necessary columns.
        """

        with self.cursor as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    sample_date TEXT,
                    location TEXT,
                    max_temp REAL,
                    min_temp REAL,                
                    mean_temp REAL
                );
            """) 
            cur.connection.commit()

    def save_data(self, data):
        """
        Saves weather data to the database for each date in the given dictionary.

        Args:
            data (str): The data to be processed.
        """

        total_records_saved = 0

        with self.cursor as cur:
            # weather_dictionary is reversed so that the oldest date for data is
            # written in the database first, and the latest weather data is 
            # inserted last
            for sample_date, temps in reversed(data.items()):
                location = 'Winnipeg'
                max_temp = temps.get('max_temp', None)
                min_temp = temps.get('min_temp', None)
                mean_temp = temps.get('mean_temp', None)

                if max_temp is not None and min_temp is not None and mean_temp is not None:
                    cur.execute("""
                        SELECT * 
                        FROM weather_data 
                        WHERE sample_date=?
                    """, (sample_date,))
                    existing_data = cur.fetchone()

                    if existing_data:
                        pass
                        # used for debugging
                        # print(f"Data already exists for {sample_date}. Skipping...")
                    else:
                        try:
                            cur.execute("""
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
                            cur.connection.commit()
                            print(f"Data saved for {sample_date}")
                            total_records_saved += 1
                        except sqlite3.Error as e:
                            print(f"Error inserting data for {sample_date}: {e}")

        if(total_records_saved == 0):
            print(f"The database is up to date as of {datetime.now().strftime('%Y-%m-%d')}. No new records added.")
        else:    
            print(f"{total_records_saved} records saved to the database.")

    def purge_data(self):
        """
        Deletes all data from the weather_data table in the database.
        """

        with self.cursor as cur:
            cur.execute('DELETE FROM weather_data')
            cur.connection.commit()
            print('All data purged from the database.')
        
    def fetch_data(self, start_date, end_date):
        """
        This method fetches all temperature data from the database for the given date range.

        Args:
            start_date (str): The start date in the format "YYYY-MM-DD".
            end_date (str): The end date in the format "YYYY-MM-DD".

        Returns:
            tuple: A tuple containing temperature data for each date in the format
            (date, max_temp, min_temp, mean_temp).
        """

        # Convert start and end dates to the correct format for the database
        start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d')

        # Create an empty list to store the temperature data for each date
        data = []

        with self.cursor as cur:
            # Loop through the dates and fetch the temperature data for each date
            while start_date_formatted <= end_date_formatted:
                sample_date = start_date_formatted.strftime('%B %d, %Y')

                # Drop leading zeroes only from the day portion of the formatted date
                sample_date = re.sub(r'(?<=\s)0', '', sample_date)
                cur.execute("""
                    SELECT max_temp, min_temp, mean_temp 
                    FROM weather_data 
                    WHERE sample_date = ?
                """, (sample_date,))
                result = cur.fetchone()

                # If the temperature data for the date exists, add it to the list
                if result:
                    max_temp, min_temp, mean_temp = result
                    data.append((sample_date, max_temp, min_temp, mean_temp))

                # Increment the date by one day
                start_date_formatted += timedelta(days=1)

        # Return the list of temperature data as a tuple
        return tuple(data)
    
    def fetch_mean_temp(self, start_date, end_date):
        """
        This method fetches mean temperature data from the database for the 
        given date range.

        Args:
            start_date (str): The start date in the format "YYYY-MM-DD".
            end_date (str): The end date in the format "YYYY-MM-DD".

        Returns:
            list: Mean Temperature data for each date 
        """

        # Convert start and end dates to the correct format for the database
        start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d')

        # Create an empty list to store the temperature data for each date
        data = []

        with self.cursor as cur:
            # Loop through the dates and fetch the temperature data for each date
            while start_date_formatted <= end_date_formatted:
                sample_date = start_date_formatted.strftime('%B %d, %Y')

                # Drop leading zeroes only from the day portion of formatted date
                sample_date = re.sub(r'(?<=\s)0', '', sample_date)
                cur.execute("""
                    SELECT mean_temp 
                    FROM weather_data 
                    WHERE sample_date = ?
                """, (sample_date,))
                result = cur.fetchone()

                # If the temperature data for the date exists, add it to the list
                if result:
                    mean_temp = result
                    data.append((sample_date, mean_temp))

                # Increment the date by one day
                start_date_formatted += timedelta(days=1)

        # Return the mean list of temperature data list
        return data

    def create_entire_database(self):
        """
        This function creates the database for the first time in order to retrieve data.
        """

        # Create a WeatherDataParser object to get the weather data
        parser = WeatherDataParser()

        # Create a DBOperations object to save the weather data to the database
        self.initialize_db()
        self.save_data(parser.get_weather_dictionary())
        print("Entire database created and records added.")
    
    def update_database(self):
        """
        Updates the weather_data table in the database with the latest data 
        from the WeatherDataParser if it is more recent than the latest data 
        in the table.
        """

        # Get the latest date in the database
        with self.cursor as cur:
            cur.execute("""
                SELECT sample_date
                FROM weather_data
                WHERE id =  (SELECT max(id) 
                             FROM weather_data)
            """)            
            latest_date = cur.fetchone()[0]
       
        latest_date = datetime.strptime(latest_date, '%B %d, %Y')
        date_after_latest = (latest_date + timedelta(days=1)).strftime('%Y-%m-%d')

        # Format date to compare to today's date
        latest_date = latest_date.strftime('%Y-%m-%d')
            
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().strftime('%Y-%m-%d')
        date_before_today = (datetime.strptime(today, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
  
        print(f"Today's date is {today}")

        # Check if the latest date in the database is older than today's date
        if latest_date < today:
            # Create a WeatherDataParser object to get the weather data
            parser = WeatherDataParser()

            # Get the new data and save it to the database 
            new_data = parser.check_for_new_data(date_after_latest, date_before_today)
            self.save_data(new_data)           
        else:
            print("Database is up to date.")        

if __name__ == "__main__":
    """
    This is the main function that instantiates a db object, and has
    functionality to parse initial data to the database. 
    """

    # # Create a DBOperations object to fetch weather data from the database
    db = DBOperations()
    # db.create_entire_database()

    # Check to see if the database has as new records to add
    db.update_database()
       
