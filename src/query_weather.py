"""
Script to generate historical hourly weather records for 
New York between 2016-01-01 and 2016-03-31.
"""
from datetime import datetime
from pathlib import Path
from meteostat import Point, Hourly

# Define file paths
BASE_PATH =  Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data" / "ny_weather_dataset.csv"

# Define variables
nyc_location = Point(40.7128, -74.0060)
start_date = datetime(2016, 1, 1)
end_date = datetime(2016, 4, 1)

def get_weather(location: Point, start: datetime, end: datetime) -> None:
    """
    Fetches hourly weather data for a specified location and time range, 
    saves it to a CSV file, and prints the save location.

    Args:
        location (Point): A `Point` object representing the geographical 
            location (latitude, longitude, and optionally elevation) 
            for which weather data is to be fetched.
        start (datetime): The start date and time for the weather data query.
        end (datetime): The end date and time for the weather data query.

    Returns:
        None: The function saves the weather data to a CSV file and prints 
        the save location. It does not return any value.
    """
    nyc_weather_hourly = Hourly(location, start, end).fetch()
    nyc_weather_hourly.to_csv(DATA_PATH)
    print(f'Saved to {DATA_PATH}')

if __name__ == "__main__":
    get_weather(location=nyc_location,
                start=start_date,
                end=end_date
                )
    