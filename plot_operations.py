import matplotlib.pyplot as plt
import numpy as np
from db_operations import DBOperations
from pprint import pprint


if __name__ == "__main__":
    db = DBOperations()

    # start_date = input("Enter a start date (YYYY-MM-DD): ")
    # end_date = input("Enter an end date (YYYY-MM-DD): ")

    # get data for several years for plotting dates hardcoded for now
    start_date = "2015-1-1"
    end_date = "2018-12-31"
    yearly_weather_data = db.fetch_data(start_date, end_date)

    # get data for one month for plotting dates hardcoded for now
    start_date = "2023-1-1"
    end_date = "2023-1-31"
    one_month__weather_data = db.fetch_data(start_date, end_date)

    print(yearly_weather_data)
    print(one_month__weather_data)

