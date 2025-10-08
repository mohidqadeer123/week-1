# Get the data from the survey project
import pandas as pd


def load_survey():
   # bring the data in as a dataframe
   url = "D:\Data_Science_Survey.csv"
   return pd.read_csv(url)