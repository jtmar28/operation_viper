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

    def fetch_monthly_year_averages(self, month):
        # get user input
        # self.year_start = input("Enter a start year (YYYY): ")
        # self.year_end = input("Enter an end year (YYYY): ")

        # hard-coded data for testing
        self.year_start = "2000"
        self.year_end = "2010"

        # get data for several years for plotting dates hardcoded for now
        year_start_date = f"{self.year_start}-1-1"
        year_end_date = f"{self.year_end}-12-31"
        yearly_weather_data = dict(db.fetch_mean_temp(year_start_date, year_end_date))
     
        values = [] 
        for key, value in yearly_weather_data.items():
            if month in key:                
                values.append(float(value[0])) 

        # Create a list of the values in new_dict
        values = list(new_dict.values())   
    
        return values

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

    month_data_list = []
    
    for i in range(1, 13):
        # Create a datetime object with year 1900, month i, and day 1
        date_obj = datetime(1900, i, 1)
        # Format the date object to a string in the %B format
        month_name = date_obj.strftime("%B")
        values = plot.fetch_monthly_year_averages(month_name) 
        month_data_list.append(values)
 
    # Create a boxplot of the values
    plt.boxplot(month_data_list )
    # plt.boxplot(month_data_list, showmeans=True, meanline=True)

    # Add a title and labels for the axes
    plt.title(f'Monthly Temperature Distribution for: {plot.year_start} to {plot.year_end}')
    plt.xlabel('Month')
    plt.ylabel('Temperature (Celsius)')

    # Show the plot
    plt.show() 

