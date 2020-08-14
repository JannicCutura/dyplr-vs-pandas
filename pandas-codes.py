
## import libraries
import pandas as pd
from nycflights13 import flights
print("This is pandas version {}. Make sure your version is >0.25 ".format(pd.__version__))




df = flights


df['avg_speed'] = df['distance'] / df['air_time']
df['LongFlight'] = df['air_time'] > 150.6865


df = df.assign(avg_speed = lambda x: x['distance']/ x['air_time']) \
        .query('air_time > 15.6865')

#change date format
#.assign(QTR = lambda x: x.QTR.dt.to_period('Q'))
df.groupby(['origin','day']).agg(
    max_airtime=pd.NamedAgg(column='air_time',aggfunc='max'),
    mean_airtime=pd.NamedAgg('air_time','mean')).reset_index()



df['mean_airtime'] = df.groupby(['origin','day'], as_index=True)['air_time'].transform('mean')
df['min_airtime'] = df.groupby(['origin','day'], as_index=True)['air_time'].transform('min')
df['max_airtime'] = df.groupby(['origin','day'], as_index=True)['air_time'].transform('max')
df['std_airtime'] = df.groupby(['origin','day'], as_index=True)['air_time'].transform('std')

# count number of times a connection was used
df['count_connections'] = df.groupby(['origin','dest'], as_index=True)['day'].transform('size')

# the same, but don't count if day is NA.
df['count_connections2'] = df.groupby(['origin','dest'], as_index=True)['day'].transform('count')





df[df.dep_delay > 150.6865]
df[df["dep_delay"] > 150.6865]










