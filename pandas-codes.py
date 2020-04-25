
## import libraries
import pandas as pd
from nycflights13 import flights


df = flights

pd.__version__
df.groupby('origin').agg(
    max_airtime = pd.NamedAgg(column='air_time',aggfunc='max'))


df2 = df.groupby('origin').agg({'air_time': ['count','mean', 'max', 'min'], 'day': ['count']})
df2['new'] = df2['air_time/count']*2
df2.columns




df2 = df2.rename(columns={'air_time/count':'test'})
df2.reset_index()

df2.describe
df2.columns.droplevel(1)
grouped_single = df.groupby('Team').agg({'Age': ['mean', 'min', 'max']})
