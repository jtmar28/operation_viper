from html.parser import HTMLParser
import urllib.request
import re

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.found_table = False
        self.td_count = 0
        self.daily_temps = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('id', 'dynamicDataTable') in attrs:
            self.found_table = True
        if self.found_table and tag == 'tr':
            self.td_count = 0
            self.daily_temps = {}

        if self.found_table and tag == 'td' and self.td_count < 3:
            self.td_count += 1
            self.is_float = False
            if self.td_count == 1:
                self.daily_temps['max_temp'] = None
            elif self.td_count == 2:
                self.daily_temps['min_temp'] = None
            else:
                self.daily_temps['mean_temp'] = None

    def handle_endtag(self, tag):
        if self.found_table and tag == 'tr':
            print(self.daily_temps)

        if self.found_table and tag == 'td' and self.td_count < 4:
            if self.is_float:
                if self.td_count == 1:
                    self.daily_temps['max_temp'] = float(self.current_data)
                elif self.td_count == 2:
                    self.daily_temps['min_temp'] = float(self.current_data)
                elif self.td_count == 3:
                    self.daily_temps['mean_temp'] = float(self.current_data)

    def handle_data(self, data):
        if self.found_table and self.td_count < 3:
            data = data.strip()
            if re.match(r'^-?\d+\.\d+$', data):
                self.is_float = True
                self.current_data = data

            if re.match(r'^-?\d+$', data) and self.td_count == 3:
                self.is_float = True
                self.current_data = data + '.0'


myparser = MyHTMLParser()

myurl = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2023&Month=3#"
with urllib.request.urlopen(myurl) as response:
    html = str(response.read())

myparser.feed(html)
