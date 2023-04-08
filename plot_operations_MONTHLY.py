import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations
from pprint import pprint

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
        self.year_start = "2018"
        self.year_end = "2023"

        # get data for several years for plotting dates hardcoded for now
        year_start_date = f"{self.year_start}-1-1"
        year_end_date = f"{self.year_end}-12-31"
        yearly_weather_data = db.fetch_data(year_start_date, year_end_date)

        return tuple(yearly_weather_data)

    def fetch_month_averages(self):
        # get user input
        # self.month_start_date = input("Enter a start date (YYYY-MM-DD): ")
        # self.month_end_date = input("Enter an end date (YYYY-MM-DD): " )
        
        # hard-coded data for testing
        self.month_start_date = "2023-1-1"
        self.month_end_date = "2023-1-31"

        # get data for one month for plotting dates hardcoded for now.
        one_month__weather_data = db.fetch_mean_temp(self.month_start_date, 
                                                     self.month_end_date)

        return one_month__weather_data     

    def plot_monthly_graph(self, month_data):
        """
        Plots a line graph of the average daily temperature for a given month.

        Args:
            :param month_data:  A list of tuples containing daily temperature 
                                data for the month.
        """
        month_dates = []
        mean_temps = []
        for date, temp in month_data:
            month_dates.append(date)
            mean_temps.append(temp[0])
        
        # pass the month_dates list and mean_temps list to the plot
        plt.plot(month_dates, mean_temps)
        plt.xlabel("Day of Month", fontsize=8)

        # Rotate x-axis labels by 45 degrees
        plt.xticks(rotation=45, fontsize=4)
        
         # set font size of y-axis label  
        plt.ylabel("Average Daily Temperature", fontsize=8)  
        plt.yticks(fontsize=4)   
        plt.title("Daily AVG Temperatures", fontsize=8)   
        plt.grid(True)  
        plt.show()

if __name__ == "__main__":
    db = DBOperations()
    plot = PlotOperations()
    
    # check for newer temperatures and update the db if so
    db.update_database()

    # fetch month data, and output the graph
    month_data = plot.fetch_month_averages()
    plot.plot_monthly_graph(month_data)
