import pandas as pd
import numpy as np

stop=pd.read_csv('Arkiv/stops.txt')
stop_times=pd.read_csv('Arkiv/stop_times.txt')
calendar=pd.read_csv('Arkiv/calendar.txt')
calendar_dates=pd.read_csv('Arkiv/calendar_dates.txt')
trips=pd.read_csv('Arkiv/trips.txt')

print(stop.shape)
print(stop_times.shape)
print(calendar.shape)
print(calendar_dates.shape)
print(trips.shape)

# ----------Conditional Subset ----------

new_calendar_dates=calendar_dates[(calendar_dates.date>20200225 )& (calendar_dates.date<20200301)]

print(new_calendar_dates.date.min())
print(new_calendar_dates.date.max())
print(new_calendar_dates.shape)


trips=trips.iloc[0:,1:3]
print(trips.head())
print(trips.shape)