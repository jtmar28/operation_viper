from html.parser import HTMLParser
from typing import Dict
import urllib.request

class WeatherDataParser(HTMLParser):
    """
    This class inherits the HTMLParser class in in order to scrape weather data
    from the climate.weather.gc.ca website.
    """
    def __init__(self):
        super().__init__()
        self.in_table = False      # Flag indicating parser is inside the table
        self.in_date_cell = False  # Flag indicating parser is inside a date cell
        self.in_temp_cell = False  # Flag indicating parser inside a temp cell
        self.current_date = None   # Currently parsed date
        self.current_temps = {}    # Current temps dictionary
        self.weather = {}          # Weather data dictionary

    def handle_starttag(self, tag, attrs):
        """
        This method searches for the appropriate div tag where the data is stored.
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
                    self.current_date = value 
                    self.current_temps = {}

        # Check if parser is inside a temperature cell and set the flag
        elif tag == "td" and self.current_temps is not None:
            self.in_temp_cell = True

    def handle_endtag(self, tag):
        """
        This method writes to the weather dictionary all of the corresponding 
        temperatures.
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
                self.weather[self.current_date] = self.current_temps
                self.current_date = None
                self.current_temps = None
        # Check if parser has exited a temperature cell and reset the flag
        elif tag == "td" and self.in_temp_cell:
            self.in_temp_cell = False

    def handle_data(self, data):
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

if __name__ == "__main__":
    parser = WeatherDataParser()

    myurl = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?\
        StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2023&Month=3#"
    with urllib.request.urlopen(myurl) as f:
        html = f.read().decode("utf-8")
        parser.feed(html)
        print(parser.weather)
