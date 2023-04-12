##
#   Group Project:  Weather Processing App
#   Course:         ADEV-3005(234116)
#   Group:          #10
#   Team members:   Dean Lorenzo, Jesse Kosowan, Justin Martinez
#   Milestone:      #1
#   Updated:        Apr 12, 2023
#

"""
This module provides functionality to parse data as outlined in the
WeatherDataParser class below.
"""
from html.parser import HTMLParser
import urllib.request
import datetime

class WeatherDataParser(HTMLParser):
    """
    This class inherits the HTMLParser class in in order to scrape weather data
    from the climate.weather.gc.ca website.
    """

    def __init__(self):
        """
        This constructor initializes the fields needed to support
        WeatherDataParser class functionality.
        """

        super().__init__()         # inherit the HTMLParser class
        self.in_table = False      # Flag indicating parser is inside the table
        self.in_date_cell = False  # Flag indicating parser is inside a date cell
        self.in_temp_cell = False  # Flag indicating parser inside a temp cell
        self.current_date = None   # Currently parsed date
        self.current_temps = {}    # Current temps dictionary
        self.weather = {}          # Weather data dictionary
        self.found_oldest_date = False # Flag showing the oldest date found

    def handle_starttag(self, tag, attrs):
        """
        This method searches for the appropriate div tag where the data is stored.

        Args:
            tag (str):      The name of the HTML tag.
            attrs (list):   A list of (name, value) tuples containing the HTML 
                            attributes and their values.
        """

        # Check if parser is inside the table and set the flag
        if tag == "div" and ("id", "dynamicDataTable") in attrs:
            self.in_table = True

        # Check if parser is inside a date cell and set the flag
        elif tag == "tr" and self.in_table:
            self.in_date_cell = True

        # Check if parser is inside an abbr tag inside a date cell, set the date
        elif tag == "abbr" and self.in_date_cell:
            for name, value in attrs:
                if name == "title":
                    try:
                        self.current_date = value
                        self.current_temps = {}
                    except:
                        pass
        # Check if parser is inside a temperature cell and set the flag
        elif tag == "td" and self.current_temps is not None:
            self.in_temp_cell = True

        # Check if parser is inside a li tag with id="nav-prev1"
        # and class="previous disabled"
        elif tag == "li" and ("id", "nav-prev1") in attrs \
            and ("class", "previous disabled") in attrs:
            self.found_oldest_date = True

    def handle_data(self, data):
        """
        This method handles the creation of the temporary current temps
        dictionary for processing daily temps.

        Args:
            data (str): The data to be processed.
        """

        # Check if parser is inside a temperature cell, current date is not
        # None, and data is a valid float
        if self.in_temp_cell and self.current_temps is not None and \
            self.current_date is not None:
            try:
                temp_value = float(data)

                # Add temperature value to current_temps dictionary if key
                # does not exist yet
                if "max_temp" not in self.current_temps:
                    self.current_temps["max_temp"] = temp_value
                elif "min_temp" not in self.current_temps:
                    self.current_temps["min_temp"] = temp_value
                elif "mean_temp" not in self.current_temps:
                    self.current_temps["mean_temp"] = temp_value
            except ValueError:
                pass

    def handle_endtag(self, tag):
        """
        This method writes to the weather dictionary all of the corresponding
        temperatures.

        Args:
            tag(str): The name of the HTML tag being parsed. 
        """

        # Check if parser has exited the table and reset the flag
        if tag == "div" and self.in_table:
            self.in_table = False

        # Check if parser has exited a date cell and reset the flag
        elif tag == "tr" and self.in_date_cell:
            self.in_date_cell = False
            # Check if current date is not None and not a non-date value and
            # add to weather data
            if self.current_date is not None and self.current_date \
                not in ["kilometres per hour", "Average", "Extreme"]:
                formattedDate = datetime.datetime.strptime(self.current_date, '%B %d, %Y')
                stringDate = formattedDate.strftime('%Y-%m-%d')
                self.current_date = stringDate
                self.weather[self.current_date] = self.current_temps
                self.current_date = None
                self.current_temps = None

        # Check if parser has exited a temperature cell and reset the flag
        elif tag == "td" and self.in_temp_cell:
            self.in_temp_cell = False

    def get_weather_dictionary(self):
        """
        This method returns the entire weather dictionary.

        Returns: A dictionary called weather.
        """

        parser = WeatherDataParser()

        # Initialize the flag
        parser.found_oldest_date = False

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        year = current_year
        month = current_month
        while True:
            myurl = (f"https://climate.weather.gc.ca/climate_data/daily_data_e.html"
                    f"?StationID=27174&timeframe=2&StartYear=1990"
                    f"&EndYear={current_year}&Day=1&Year={year}&Month={month}")

            print(f"Parsing data for {datetime.date(year, month, 1).strftime('%B %Y')}")

            with urllib.request.urlopen(myurl) as request:
                html = request.read().decode("utf-8")
                parser.feed(html)
                if parser.found_oldest_date:
                    break
                month -= 1
                if month == 0:
                    month = 12
                    year -= 1

        print("Weather dictionary data scrape complete.")
        return parser.weather

    def check_for_new_data(self, start_date, end_date):
        """
        Parses new data from the website for all the dates between start_date and end_date.
        Prints the data line by line.

        Args:
            start_date (str): Start date in the format "YYYY-MM-DD".
            end_date (str): End date in the format "YYYY-MM-DD".

        Returns:
            dict: A dictionary containing the weather data for all the dates parsed.
        """
        parser = WeatherDataParser()

        # Convert start_date and end_date to datetime objects
        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        # Initialize current_date to start_date
        current_date = start_datetime

        # Iterate over the days from start_date to end_date
        while current_date <= end_datetime:
            # Construct the URL for the current date
            my_url = (f"https://climate.weather.gc.ca/climate_data/daily_data_e.html"
                    f"?StationID=27174&timeframe=2&StartYear={current_date.year}"
                    f"&EndYear={current_date.year}&Day={current_date.day}"
                    f"&Year={current_date.year}&Month={current_date.month}")

            # Print a message to indicate the date being parsed
            print(f"Parsing data for {current_date.strftime('%B %d, %Y')}")

            # Use urllib.request to retrieve the HTML content for the current date
            with urllib.request.urlopen(my_url) as request:
                html = request.read().decode("utf-8")

                # Feed the HTML content to the parser
                parser.feed(html)

                # If the current date is within the range of start_date and end_date,
                # print the weather data for that date line by line
                for date_str in parser.weather.keys():
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    if start_datetime.date() <= date <= end_datetime.date() \
                        and date == current_date.date():
                        weather_data = parser.weather[date_str]
                        for key, value in weather_data.items():
                            print(f"{key}: {value}")

            # Move on to the next day
            current_date += datetime.timedelta(days=1)

        return parser.weather    

if __name__ == "__main__":
    # Create a new instance of the WeatherDataParser class
    weather_dictionary = WeatherDataParser()

    # Call the get_weather_dictionary method to parse weather data from the
    # website and return a dictionary containing the data for each date
    weather_data = weather_dictionary.get_weather_dictionary()

    # Print the weather data dictionary to the console
    print(weather_data)
