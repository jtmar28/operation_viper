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

    def fetch_monthly_year_averages(self, month, year_start_date, year_end_date):
        # hard-coded data for testing and debugging only
        # self.year_start = "2000"
        # self.year_end = "2017"
        
        yearly_weather_data = dict(db.fetch_mean_temp(year_start_date, year_end_date))
    
        new_dict = {}
        values = [] 
        for key, value in yearly_weather_data.items():
            if month in key:                
                values.append(float(value[0]))
                new_dict[key] = values[-1]

        # Create a list of the values in new_dict
        values = list(new_dict.values())   
    
        return values
    
    def plot_yearly_graph(self):
        # list to store all of the mean data for each month within the year range
        month_data_list = []

        # get user input
        self.year_start = input("Enter a start year (YYYY): ")
        self.year_end = input("Enter an end year (YYYY): ")

        # get data for several years for plotting dates hardcoded for now
        start_date = f"{self.year_start}-1-1"
        end_date = f"{self.year_end}-12-31"
        
        for i in range(1, 13):
            # Create a datetime object with year 1900, month i, and day 1
            date_obj = datetime(1900, i, 1)

            # Format the date object to a string in the %B format
            month_name = date_obj.strftime("%B")
            values = self.fetch_monthly_year_averages(month_name, start_date, end_date) 
            month_data_list.append(values)

        plt.boxplot(month_data_list ) 

        # Add a title and labels for the axes
        plt.title(f'Monthly Temperature Distribution for: {self.year_start} to {self.year_end}')
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')

        # Show the plot
        plt.show() 

if __name__ == "__main__":
    db = DBOperations()
    plot = PlotOperations()

    plot.plot_yearly_graph()

    
