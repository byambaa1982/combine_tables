# Combining multitables on key

## Goal
One of my customers sent me the following message on fiverr: `I need help creating one table/CSV-file from a few different tables (in GTFS-format).` 
There are three different tables. `trips.txt calendar.txt and stop_times.txt`. The goal is that we needed to combine them and made some data engineering. 

### Calendar dates

  index  | service_id    | date     | exception_type
-------- | ------------- | -------- | --------------
0   | 1             | 20200205 | 1
1   | 1 	    | 20200206 | 1
2   | 1             | 20200207 | 1
3   | 1             | 20200212 | 1


### Trips

![trips](/images/trips.png)

### Stop times

![stop times](/images/stop_times.png)

### My goal

![Final](/images/final.png)

The following is all the tables we need to do:

	stop_times=pd.read_csv('Arkiv/stop_times.txt')
	calendar_dates=pd.read_csv('Arkiv/calendar_dates.txt')
	trips=pd.read_csv('Arkiv/trips.txt')

Our customer needs only trip data between Feb 25, 2020 and March 01, 2020. So we need to select calender dates Dataframe by condition on date column. 

	new_calendar_dates=calendar_dates[(calendar_dates.date>20200225 )& (calendar_dates.date<20200301)]

Also, We need only the first five columns from `Stop times`. 

	new_csv=stop_times.iloc[0:,0:5]

After that I merged them on service_id and make a new column named "unique_trip_id"

	a=trips
	b=new_calendar_dates
	c=pd.merge(a, b, on='service_id', how='left')
	c['unique_trip_id']=c.index+1
	e=stop_times
	f=pd.merge(c, e, on='trip_id', how='left')
	df=f
We cannot combine columns have intiger data. We have to turn `int` values into `str` values before combine.

	df['unique_trip_id']=df['unique_trip_id'].map(lambda x: x+1)
	df['first']=df['unique_trip_id'].map(lambda x: str(x))
	df['second']=df['stop_sequence'].map(lambda x: str(x))
	df['first_date']=df['start_date'].map(lambda x: str(x))
	df['second_date']=df['end_date'].map(lambda x: str(x))
	df['unique_sub_trip_id']= df[['first', 'second']].apply(lambda x: '.'.join(x), axis=1)
	df['arrival_time']= df[['second_date', 'arrival_time']].apply(lambda x: ' '.join(x), axis=1)
	df['departure_time']= df[['first_date', 'departure_time']].apply(lambda x: ' '.join(x), axis=1)

As our customer's wish, we have to rearrange Pandas column sequence. 

	df=df[['unique_trip_id','unique_sub_trip_id','trip_id','stop_id','stop_sequence','arrival_time','departure_time']]

The most challenging part of this task is that we have to shift down `arrival_time` and `stop_sequence` by one. But it is not a whole dataset but it consists many subsets by `unique_trip_id`. We have to use `shift` method on each subset seprately. 


	unique_trip_id_list=df.unique_trip_id.unique().tolist()

	df_list=[]
	for i in unique_trip_id_list:
	  df1 = df.loc[df['unique_trip_id'] == i]
	  df1['arrival_time'] = df1['arrival_time'].shift(-1)
	  df1['stop_sequence'] = df1['stop_sequence'].shift(-1)
	  df_list.append(df1)
	final_result=pd.concat(df_list)

Here we go. This is our file to deliver to the customer. 

	final_result.to_csv('result.csv')

If you have anything to ask, please contact me clicking following link? 

www.fiverr.com/coderjs

Thank you
