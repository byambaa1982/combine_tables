import pandas as pd
import numpy as np

# -------  Read CSV data ----------


# stop=pd.read_csv('Arkiv/stops.txt')
stop_times=pd.read_csv('Arkiv/stop_times.txt')
# calendar=pd.read_csv('Arkiv/calendar.txt')
calendar_dates=pd.read_csv('Arkiv/calendar_dates.txt')
trips=pd.read_csv('Arkiv/trips.txt')

# ----------Conditional Subset ----------

new_calendar_dates=calendar_dates[(calendar_dates.date>20200225 )& (calendar_dates.date<20200301)]



#----------- remove useless columns from calendar data----------------------------

new_csv=stop_times.iloc[0:,0:5]


# ---------------Merge them on service_id and make a new column named "unique_trip_id"
a=trips
b=new_calendar_dates
c=pd.merge(a, b, on='service_id', how='left')
c['unique_trip_id']=c.index+1
e=stop_times
f=pd.merge(c, e, on='trip_id', how='left')
df=f




# result['unique_trip_id'] = result.groupby(['trip_id','end_date']).ngroup()
# result=result.sort_values(by=['unique_trip_id', 'stop_sequence'])


# unique_trip_id=1
# new=[]
# for i in range(0,len(my_list)-1):
#   if my_list[i] == my_list[i+1]:
#     new.append(unique_trip_id)
#   else:
#     unique_trip_id+=1
#     new.append(unique_trip_id)

#  -------- Make int into string and combine two column on new columns-------


df['unique_trip_id']=df['unique_trip_id'].map(lambda x: x+1)
df['first']=df['unique_trip_id'].map(lambda x: str(x))
df['second']=df['stop_sequence'].map(lambda x: str(x))
df['first_date']=df['start_date'].map(lambda x: str(x))
df['second_date']=df['end_date'].map(lambda x: str(x))
df['unique_sub_trip_id']= df[['first', 'second']].apply(lambda x: '.'.join(x), axis=1)
df['arrival_time']= df[['second_date', 'arrival_time']].apply(lambda x: ' '.join(x), axis=1)
df['departure_time']= df[['first_date', 'departure_time']].apply(lambda x: ' '.join(x), axis=1)

# --------- Rerange data ---------------

df=df[['unique_trip_id','unique_sub_trip_id','trip_id','stop_id','stop_sequence','arrival_time','departure_time']]

unique_trip_id_list=df.unique_trip_id.unique().tolist()

df_list=[]
for i in unique_trip_id_list:
  df1 = df.loc[df['unique_trip_id'] == i]
  df1['arrival_time'] = df1['arrival_time'].shift(-1)
  df1['stop_sequence'] = df1['stop_sequence'].shift(-1)
  df_list.append(df1)
final_result=pd.concat(df_list)

final_result.to_csv('result.csv')
