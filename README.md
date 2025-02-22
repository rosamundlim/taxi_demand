## Business Problem

Using the New York Taxi Dataset from January to March 2016, identify high-demand areas where drivers are more likely to secure rides. This analysis will help Taxi Drivers with trip planning so as to maximise their earnings. 

## Technical Introduction

I will frame this as a supervised time series problem. I will use historical records to predict next hour's taxi demand for each location.

In this repository, I use the Polars library to manipulate and implement feature engineering 
on ~34.5 million taxi trip records for New York (1 Jan 2016 to 31 Mar 2016). 

Polars is a high-performance DataFrame library designed for handling large datasets efficiently using Rust. It leverages Apache Arrow for memory-efficient columnar data representation. Unlike Pandas, which processes data row by row, Polars operates with a multi-threaded, vectorized engine, making it significantly faster, especially for complex operations on large datasets. 

With Polars, I can efficiently downsample and aggregate my data from ~34.5 million rows to ~5 million rows so that it avoids over granularity and highlights temporal patterns. 

For Modelling, I used Linear Regression and XGBoost Regressor (Poisson objective function) to predict next hour's pickup demand for each location. 

## Tech Stack

 - Preprocessing and Feature Engineering: Polars, Pandas, Meteostat
 - Modelling: Scikit-learn, XGBoost
 - Model Interpretability & Analysis: LIME, Tableau
 - Version Control: Git 

## Directory Structure 

```
.
└── taxi_demand/
    ├── data/ (ignored by git to prevent bloating)
    │   ├── yellow_tripdata_2016-01.csv
    │   ├── yellow_tripdata_2016-02.csv
    │   ├── yellow_tripdata_2016-03.csv
    │   └── feature_engineered_dataset.csv
    ├── models/
    │   ├── linear_reg_model.joblib
    │   └── xgboost_model.json
    ├── predictions/
    │   ├── lime_explanation_iloc06.html
    │   └── prediction_df_xgboost.csv
    ├── src/
    │   ├── __init__.py
    │   ├── clean_data.py
    │   └── query_weather.py
    ├── eda_feature_engineering.ipynb
    ├── linear_regression.ipynb
    ├── xgboost.ipynb
    ├── README.md
    └── requirements.txt
```

- `data/feature_engineered_dataset.csv`: Cleaned and aggregated dataset with feature engineered variables
- `models/`: contains the trained models for the ML task, including linear regression (baseline) and XGBoost regression model
- `predictions/`: `prediction_df_xgboost.csv` which contains the next hour taxi demand prediction. `lime_explanation_iloc06.html` lime explanation for the prediction for 6th row in the test set. 
- `src/`: `clean_data.py` is a script using Polars to clean and aggregate data for Feb and Mar 2016 records. `query_weather.py` is a script that calls Meteostat to generate a weather information table which is later joined with trip records on datetime column
- `eda_feature_engineering.ipynb`: notebook with cleaning and feature engineering for the ML task
- `linear_regression.ipynb`: notebook for training a baseline linear regression model
- `xgboost.ipynb`: notebook for training xgboost regressor model
- `requirements.txt`: list of required libraries and dependencies to run this prediction task.

## Deployment

Using the inference result, I created a tableau heatmap to serve the next hour predictions from March 16 to March 31 2016. 
View the visualisation [here](https://public.tableau.com/app/profile/rosamund5307/viz/taxi_demand_predictions_xgboost/NextHourTaxiDemandPrediction) 
