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

        # Check if parser is inside a li tag with id="nav-prev1" 
        # and class="previous disabled"
        elif tag == "li" and ("id", "nav-prev1") in attrs \
            and ("class", "previous disabled") in attrs:
            self.found_oldest_date = True
 
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
        """
        This method handles the creation of the temporary current temps
        dictionary for processing daily temps.
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

    def get_starttag_text(self):
        """
        This method returns the text of the start tag that caused the
        callback and is used to identify the oldest date that weather is stored.
        """

        return self.rawdata[self.offset:self.offset + self.length].lower()

if __name__ == "__main__":
    parser = WeatherDataParser()
    parser.found_oldest_date = False  # Initialize the flag

    current_month = datetime.datetime.now().month
    current_date = datetime.datetime.now().day
    current_year = datetime.datetime.now().year

    print(f"\nToday's date: {current_month}/{current_date}/{current_year}\n")

    year = current_year
    month = current_month
    while True:
        myurl = (f"https://climate.weather.gc.ca/climate_data/daily_data_e.html"
                 f"?StationID=27174&timeframe=2&StartYear=1840"
                 f"&EndYear={current_year}&Day=1&Year={year}&Month={month}")

        with urllib.request.urlopen(myurl) as f:
            html = f.read().decode("utf-8")
            parser.feed(html)
            print(f"Processing weather data for {month}/{year}")  
            
            # Check if oldest date is found
            if ('li', 'nav-prev1') in parser.getpos() and ('class', 
                'previous disabled') in parser.get_starttag_text():
                parser.found_oldest_date = True
                break

        # decrement year and month to move to previous month's data
        month -= 1
        if month == 0:
            year -= 1
            month = 12
        
        # Exit the while loop if the oldest date has been found
        if parser.found_oldest_date:
            break

    print("Finished processing.")
    print("Final weather data:")
    print(parser.weather)
