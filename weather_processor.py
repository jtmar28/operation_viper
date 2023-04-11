"""Contains the WeatherProcessor class, which handles events and controls
   several other modules, which together scrape, store, and plot weather data."""
import threading
from pubsub import pub
import wx
from frm_main import frmMain
from db_operations import DBOperations
from plot_operations import PlotOperations
from scrape_weather import WeatherScraper

class WeatherProcessor(frmMain):
    """Contains functions to handle events when the download or plot buttons are pressed."""

    def __init__(self):
        """Initializes the frame."""
        frmMain.__init__(self, None)

    def download(self, event):
        """
        Downloads either missing or all data to the database.
        """
        self.lblStatus.SetLabel("Status: Downloading data...")

        download = self.choiceData.GetSelection()
        database = DBOperations("weather_database.sqlite")
        if download == 0:
            last_date = database.fetch_last_date()
            scraper = WeatherScraper(last_date)
        else:
            database.purge_data()
            database.initialize_db()
            scraper = WeatherScraper()

        pub.subscribe(self.download_complete, "data")
        pub.subscribe(self.update_status, "progress")
        scrape_thread = threading.Thread(daemon=True, target=scraper.scrape)
        scrape_thread.start()


    def download_complete(self, weather_data):
        """
        Recieves weather data from the scraper thread, then saves it to the database.
        """
        database = DBOperations("weather_database.sqlite")
        database.save_data(weather_data)
        self.lblStatus.SetLabel("Status: Download complete!")


    def update_status(self, progress):
        """
        Recieves status updates from the scraper thread, and displays them in the UI.
        """
        self.lblStatus.SetLabel("Status: " + progress)


    def plot_daily_temps(self, event):
        """
        Displays the daily mean temps for a given month in a given year as a line plot.
        """

        year = self.txtDailyYear.GetValue()
        month = self.txtDailyMonth.GetValue()

        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-31"

        database = DBOperations("weather_database.sqlite")

        weather_data = database.fetch_data(start_date, end_date)

        operations = PlotOperations()
        operations.plot_daily(weather_data)


    def plot_monthly_temps(self, event):
        """
        Displays the mean temps of the months in a given year range as a box plot.
        """
  
        start_year = self.txtStartYear.GetValue()
        end_year = self.txtEndYear.GetValue()

        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"

        database = DBOperations("weather_database.sqlite")

        weather_data = database.fetch_data(start_date, end_date)

        operations = PlotOperations()
        operations.plot_monthly(weather_data, start_year, end_year)


if __name__ == "__main__":
            
    app = wx.App()

    frm = WeatherProcessor()

    frm.Show()

    app.MainLoop()
