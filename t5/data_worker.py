import pandas as pd
import requests


def get_data(url, api_key):
    r = requests.get(url)
    print(r)


def get_pd(path):
    return pd.read_csv(path)


if __name__ == '__main__':

    URL = "https://api.covidactnow.org/v2/states.timeseries.json?apiKey=3856b633126e4a27b2e45516c9290395"
    get_data(URL, 'a')

    PATH = "data/states.timeseries.csv"

    df_states = get_pd(PATH)

    print(df_states)
