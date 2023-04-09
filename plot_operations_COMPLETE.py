import matplotlib.pyplot as plt
from db_operations import DBOperations
from datetime import datetime

class PlotOperations:
    def __init__(self):
        self.year_start = ""
        self.year_end = ""
        self.month_start_date = ""
        self.month_end_date = ""

        #instantiate a DBOperations object
        self.db = DBOperations()

    def fetch_monthly_year_averages(self, month, year_start_date, year_end_date):
        
        # converts the data to a dictionary of mean temps
        yearly_weather_data = dict(self.db.fetch_mean_temp(year_start_date, year_end_date))
    
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

        print("Processing yearly graph...")

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

    def fetch_month_averages(self):
        # get user input
        self.month_start_date = input("Enter a start date (YYYY-MM-DD): ")
        self.month_end_date = input("Enter an end date (YYYY-MM-DD): ")
        
        # hard-coded data for testing, remains in code 
        # self.month_start_date = "2023-1-1"
        # self.month_end_date = "2023-1-31"

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
        plt.xticks(rotation=45, fontsize=4)
        
        # set font size of y-axis label  
        plt.ylabel("Average Daily Temperature", fontsize=8)  
        plt.yticks(fontsize=4)   
        plt.title("Daily AVG Temperatures", fontsize=8)   
        plt.grid(True)  
        plt.show()

if __name__ == "__main__":
    """
    Main function instantiates a DBOperations object, and two PlotOperations
    objects one for a monthly plot, and a yearly plot. After aggregating
    data, the graphs output to the screee one at a time.
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
        