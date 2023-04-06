import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations
from pprint import pprint
from datetime import datetime

class PlotOperations:
    def __init__(self):
        self.year_start = ""
        self.year_end = ""
        self.month_start_date = ""
        self.month_end_date = ""

    def fetch_yearly_averages(self):
        # get user input
        # self.year_start = input("Enter a start year (YYYY): ")
        # self.year_end = input("Enter an end year (YYYY): ")

        # hard-coded data for testing
        self.year_start = "2015"
        self.year_end = "2023"

        # get data for several years for plotting dates hardcoded for now
        year_start_date = f"{self.year_start}-1-1"
        year_end_date = f"{self.year_end}-12-31"
        yearly_weather_data = db.fetch_data(year_start_date, year_end_date)

        # return tuple(yearly_weather_data)

        # create a dictionary of lists
        # the dictionary key will be the month
        # the data in the list will be the mean temp for each day of that month
        weather_data = {} # initialize weather data dictionary
        # loop over each month ranging from 1-12
        for month in range(1, 13):
            # for each month, initialize a new month_data list
            # data[3] is the fourth element of the data tuple (mean temp).
            # the if statement checks if the month of the date in data[0] is equal to the month variable.
            # if it is... data[3] (the mean temp) is added to the list for that month.
            month_data = [data[3] for data in yearly_weather_data if datetime.strptime(data[0], '%B %d, %Y').month == month]
            weather_data[month] = month_data # add this loops month key-value pair to the dictionary.

        return weather_data



    def fetch_month_averages(self):
        # get user input
        # self.month_start_date = input("Enter a start date (YYYY-MM-DD): ")
        # self.month_end_date = input("Enter an end date (YYYY-MM-DD): " )

        # hard-coded data for testing
        self.month_start_date = "2023-1-1"
        self.month_end_date = "2023-1-31"

        # get data for one month for plotting dates hardcoded for now
        one_month__weather_data = db.fetch_data(self.month_start_date, self.month_end_date)

        return tuple(one_month__weather_data)


if __name__ == "__main__":
    db = DBOperations()
    plot = PlotOperations()

    # pprint(plot.fetch_month_averages())
    pprint(plot.fetch_yearly_averages())

