##
#   Group Project:  Weather Processing App
#   Course:         ADEV-3005(234116)
#   Group:          #10
#   Team members:   Dean Lorenzo, Jesse Kosowan
#   Milestone:      #3
#   Updated:        Apr 11, 2023 
#

import matplotlib.pyplot as plt
from db_operations import DBOperations
from datetime import datetime

class PlotOperations:
    """
    This class adds functionality to the Weather App by outputting graphical data
    to the screen.
    """
    def __init__(self):
        """
        Initializes an instance of the class with the following instance variables:
        - year_start: a string representing the start year
        - year_end: a string representing the end year
        - month_start_date: a string representing the start date of the month
        - month_end_date: a string representing the end date of the month
        - db: an instance of the DBOperations class
        """

        self.year_start = ""
        self.year_end = ""
        self.month_start_date = ""
        self.month_end_date = ""
        self.db = DBOperations()

    def fetch_monthly_year_averages(self, month, year_start_date, year_end_date):
        """
        Fetches the monthly year averages for a given month within a given date range.
        
        Args:
        - month: a string representing the month (e.g., "January", "February", etc.)
        - year_start_date: a string representing the start date of the year in YYYY-MM-DD format
        - year_end_date: a string representing the end date of the year in YYYY-MM-DD format
        
        Returns:
        - A list of the monthly year averages for the given month within the given date range20
        """
        
        # converts the data to a dictionary of mean temps
        yearly_weather_data = dict(self.db.fetch_mean_temp(year_start_date, year_end_date))
   
        new_dict = {}
        values = [] 
        for key, value in yearly_weather_data.items():
            # compare the 2-digit string month to the key's 2-digit string month
            if month in key[5:7]:                
                values.append(float(value[0]))
                new_dict[key] = values[-1]

        # Create a list of the values in new_dict
        values = list(new_dict.values())   

        return values

    def plot_yearly_graph(self):
        """
        Plots a boxplot of the monthly temperature distributions for a given year range.

        Prompts the user to enter a start year and an end year, and retrieves the average
        monthly temperature data for each month within the year range from the database.
        The temperature data for each month is then plotted as a boxplot.
        """

        # list to store all of the mean data for each month within the year range
        month_data_list = []

        # get user input and validate
        while True:
            try:
                self.year_start = int(input("Enter a start year (YYYY): "))
                if len(str(self.year_start)) != 4:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please enter a valid 4-digit year.")

        while True:
            try:
                self.year_end = int(input("Enter an end year (YYYY): "))
                if len(str(self.year_end)) != 4:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input! Please enter a valid 4-digit year.")

        print("Processing yearly graph...")

        # get data for several years for plotting dates
        start_date = f"{self.year_start}-1-1"
        end_date = f"{self.year_end}-12-31"
        
        for i in range(1, 13):
            # Create a datetime object with year 1900, month i, and day 1
            date_obj = datetime(1900, i, 1)

            # Format the date object to a string in the 'MM' format
            month = date_obj.strftime("%m")
            values = self.fetch_monthly_year_averages \
                (month, start_date, end_date) 
            month_data_list.append(values)

        plt.boxplot(month_data_list) 

        # Add a title and labels for the axes
        plt.title(f'Monthly Temperature Distribution for: '
                  f'{self.year_start} to {self.year_end}')
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')

        # Show the plot
        plt.show()  

    def fetch_month_averages(self):
        """
        Fetches the average daily temperature data for a given month.

        Prompts the user to enter a start date and an end date for the month, 
        and retrieves the average daily temperature data for that month from
        the database.

        Returns:
            A list of tuples containing daily temperature data for the month.
        """

        # get user input and validate
        while True:
            self.month_start_date = input("Enter a start date (YYYY-MM-DD): ")
            try:
                datetime.strptime(self.month_start_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid input! Please enter a valid date in the format "
                      "YYYY-MM-DD.")

        while True:
            self.month_end_date = input("Enter an end date (YYYY-MM-DD): ")
            try:
                datetime.strptime(self.month_end_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid input! Please enter a valid date in the format "
                      "YYYY-MM-DD.")

        # get data for one month for plotting dates hardcoded for now.
        one_month__weather_data = self.db.fetch_mean_temp(self.month_start_date, 
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
        plt.xticks(rotation=45, fontsize=5)
        
        # set font size of y-axis label  
        plt.ylabel("Average Daily Temperature", fontsize=8)  
        plt.yticks(fontsize=4)   
        plt.title("Daily AVG Temperatures", fontsize=8)   
        plt.grid(True)  
        plt.show()

if __name__ == "__main__":
    """
    Main function instantiates two PlotOperations objects one for a monthly 
    plot, and a yearly plot. After aggregating data, the graphs output to the 
    screen one at a time.
    """
    
    plot_monthly = PlotOperations()
    plot_yearly = PlotOperations()

    # check for newer temperatures and update the db if so
    plot_monthly.db.update_database()

    # fetch yearly data, and output graph
    plot_yearly.plot_yearly_graph()

    # fetch month data, and output the graph
    month_data = plot_monthly.fetch_month_averages()
    plot_monthly.plot_monthly_graph(month_data)        
