"""Contains pipeline to clean data"""
import logging
from typing import List
import polars as pl

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",  # Log message format
)

class CleanData:
    """Pipeline to clean dataset"""
    def __init__(self,
                 df: pl.DataFrame,
                 cols_to_keep: List,
                 pickup_datetime_col: str
                 ):
        self.df = df
        self.datetime_col = pickup_datetime_col
        self.cols_to_keep = cols_to_keep

    def select_columns(self) -> None:
        """Selects a list of priority columns
        """
        self.df = self.df.select(self.cols_to_keep)
        logging.info("df shape after keeping priority cols: %s", self.df.shape)

    def remove_null_island(self) -> None:
        """Remove rows where latitude and longitude are 0.0
        """
        rows_before = self.df.shape[0]
        self.df =  self.df.filter(~(
                                    (pl.col('pickup_longitude')==0.0) & \
                                    (pl.col('pickup_latitude')==0.0)
                                    )
        )
        rows_after = self.df.shape[0]
        rows_removed = rows_before - rows_after
        logging.info("df shape after removing nulls: %s", self.df.shape)
        logging.info("removed %d null island rows", rows_removed)

    def remove_outside_ny(self) -> None:
        """Filters out location outside of New York bounding box.
        Reference: https://observablehq.com/@rdmurphy/u-s-state-bounding-boxes
        """
        rows_before = self.df.shape[0]
        nyc_top = 45.01550900568005
        nyc_bottom = 40.502009391283906
        nyc_left = -79.7633786294863
        nyc_right = -71.85616396303963

        self.df = self.df.filter(
            ~(
                (pl.col("pickup_latitude") < nyc_bottom) |
                (pl.col("pickup_latitude") > nyc_top) |
                (pl.col("pickup_longitude") < nyc_left) |
                (pl.col("pickup_longitude") > nyc_right)
            )
        )
        rows_after = self.df.shape[0]
        rows_removed = rows_before - rows_after
        logging.info("df shape after keeping priority cols: %s", self.df.shape)
        logging.info("Removed %d rows outside New York", rows_removed)

    def downsample_1h(self) -> None:
        """Downsamples pickup datetime to hourly intervals and aggregates
        pickup count at hourly intervals
        """
        logging.info("Downsampling into 1h intervals and aggregating hourly"
              " pickup count by location")
        self.df = self.df.sort(self.datetime_col)
        self.df = self.df.with_columns(
            pl.col("pickup_longitude").round(3),
            pl.col("pickup_latitude").round(3),
        )
        self.df = self.df.group_by_dynamic("tpep_pickup_datetime",
                                         every="1h",
                                         group_by=["pickup_longitude", "pickup_latitude"]\
                                        ).agg(pl.len().alias("current_pickup_count"))

    def clean_pipeline(self):
        """main method to clean the DataFrame with the following steps:
        i. Keep priority columns,
        ii. Remove rows with null coordinates
        iii. Remove rows where coordinates are outside New York
        iv. Downsample to 1 hour intervals
        """
        self.select_columns()
        self.remove_null_island()
        self.remove_outside_ny()
        self.downsample_1h()
        logging.info("Cleaning completed, current shape of df: %s", self.df.shape)
        return self.df
