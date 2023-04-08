import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations
from pprint import pprint
from datetime import datetime
import statistics

class PlotOperations:
    def __init__(self):
        self.year_start = ""
        self.year_end = ""
        self.month_start_date = ""
        self.month_end_date = ""

    def fetch_monthly_year_averages(self, month):
        # get user input
        # self.year_start = input("Enter a start year (YYYY): ")
        # self.year_end = input("Enter an end year (YYYY): ")

        # hard-coded data for testing
        self.year_start = "2020"
        self.year_end = "2023"

        # get data for several years for plotting dates hardcoded for now
        year_start_date = f"{self.year_start}-1-1"
        year_end_date = f"{self.year_end}-12-31"
        yearly_weather_data = dict(db.fetch_mean_temp(year_start_date, year_end_date))

        new_dict = {}
        values = []
        outliers = []

        for key, value in yearly_weather_data.items():
            if month in key:
                values.append(float(value[0]))
                new_dict[key] = values[-1]

        # accuracy to 1 decimal point        
        mean = round(statistics.mean(values), 1)
        if (mean > 0):
            box_top = round(mean * 1.25, 1)
            box_bottom = round(mean * 0.75, 1)
            maximum = round(1.25 * box_top, 1)
            minimum = round(box_bottom * 0.75, 1)
        else:
            box_bottom = round(mean * 1.25, 1)
            box_top = round(mean * 0.75, 1)
            minimum = round(.75 * box_top, 1)
            maximum = round(box_bottom * 1.25, 1)
            
        print(f"{month}: mean = {mean} box_top = {box_top} box_bottom = {box_bottom} maximum = {maximum} minimum = {minimum}")

        return yearly_weather_data

       
 



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

    # fetch average of the month of February
    plot.fetch_monthly_year_averages('January')

