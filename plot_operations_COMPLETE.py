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
        self.year_end = "2017"

        # get data for several years for plotting dates hardcoded for now
        year_start_date = f"{self.year_start}-1-1"
        year_end_date = f"{self.year_end}-12-31"
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

        print("Processing yearly graph...")
        month_data_list = []
        
        for i in range(1, 13):
            # create a datetime object with year 1900, month i, and day 1
            date_obj = datetime(1900, i, 1)

            # format the date object to a string in the %B format
            month_name = date_obj.strftime("%B")

            # invoke the method to get the monthly year averages by month
            values = self.fetch_monthly_year_averages(month_name) 
            month_data_list.append(values)
    
        # Create a boxplot of the values
        plt.boxplot(month_data_list) 

        # Add a title and labels for the axes
        plt.title(f'Monthly Temperature Distribution for: {self.year_start} to {self.year_end}')
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')

        # Show the plot
        plt.show() 

    def fetch_month_averages(self):
        # get user input
        # self.month_start_date = input("Enter a start date (YYYY-MM-DD): ")
        # self.month_end_date = input("Enter an end date (YYYY-MM-DD): ")
        
        # hard-coded data for testing, remains in code 
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

        print("Processing monthly graph...")

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
    plot_monthly = PlotOperations()
    plot_yearly = PlotOperations()

    # check for newer temperatures and update the db if so
    db.update_database()

    # output the yearly graph
    plot_yearly.plot_yearly_graph()
    
    # fetch month data, and output the graph
    month_data = plot_monthly.fetch_month_averages()
    plot_monthly.plot_monthly_graph(month_data)
        