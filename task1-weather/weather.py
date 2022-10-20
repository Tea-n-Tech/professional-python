import requests
import json
import datetime
import pandas as pd


# get time in right format for next three days
current_day = datetime.date.today()
end_date = current_day + datetime.timedelta(days=3)

current_day = current_day.isoformat()
end_date = end_date.isoformat()

#right the url for api call with right info to fetch
api_url = 'https://api.open-meteo.com/v1/forecast?latitude=48.77&longitude=2.42&daily=temperature_2m_max&daily=temperature_2m_min&daily=precipitation_sum&timezone=auto&start_date={}&end_date={}'.format(current_day, end_date)

#put in dataframe for easier display and read in console
response = requests.get(api_url)
weather_data = json.loads(response.text)
weather_df = pd.DataFrame.from_dict(weather_data)


print(weather_df[["timezone", "daily_units", "daily"]])
