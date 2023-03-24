from html.parser import HTMLParser
import urllib.request

class WeatherScraper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.in_th = False
        self.row_data = []

        # Create a dictionary of dictionaries to contain output information.

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            # print("Start tag:", tag)
            self.in_table = True
        elif self.in_table and tag == 'tbody':
            # print("Start tag:", tag)
            self.in_tbody = True
        elif self.in_tbody and tag == "tr":
            # print("Start tag:", tag)
            self.in_tr = True
        elif self.in_tr and tag == "th":
            # print("Start tag:", tag)
            self.in_th = True
        elif self.in_tr and tag == "td":
            # print("Start tag:", tag)
            self.in_td = True

    def handle_endtag(self, tag):
        if tag == 'table':
          # print("End tag", tag)
          self.in_table = False
        elif self.in_tbody and tag == "tbody":
            # print("End tag:", tag)
            self.in_tbody = False
        elif self.in_tr and tag == "tr":
            # print("End tag:", tag)
            self.in_tr = False
        elif self.in_th and tag == "th":
            # print("End tag:", tag)
            self.in_th = False
        elif self.in_td and tag == "td":
            # print("End tag", tag)
            self.in_td = False

    def handle_data(self, data):
        if self.in_table and self.in_tr and self.in_th:
          # for each row in table minus (len(table) - 4)
          print("Date of month:", data)
        elif self.in_table and self.in_tr and self.in_td:
          self.row_data.append(data.strip())
          if len(self.row_data) == 13:
              min_temp = self.row_data[0]
              max_temp = self.row_data[1]
              mean_temp = self.row_data[2]
              print(f"Max Temp: {min_temp} Min Temp: {max_temp} Mean Temp: {mean_temp}")
              self.row_data = []

myparser = WeatherScraper()

# Dynamically find date for url

# with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5') as response:
#     html = str(response.read())
year = 2018
month = 5

url_template = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={}&Month={}'

url = url_template.format(year, month)

with urllib.request.urlopen(url) as response:
    html = str(response.read())

myparser.feed(html)
