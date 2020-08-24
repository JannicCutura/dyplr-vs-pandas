
## import libraries
import numpy as np
import pandas as pd
import time
from nycflights13 import flights
print("This is pandas version {}. Make sure your version is >0.25 ".format(pd.__version__))

def csnap(df, fn=lambda x: x.shape, msg=None):
    """ Custom Help function to print things in method chaining.
        Returns back the df to further use in chaining.
        Credits: https://towardsdatascience.com/the-unreasonable-effectiveness-of-method-chaining-in-pandas-15c2109e3c69
    """
    if msg:
        print(msg)
    display(fn(df))
    return df


df = flights

df.head()

df.columns


df = flights

df = df.pipe(csnap,  msg="Let's start") \
       .assign(avg_speed = lambda x: x['distance']/ x['air_time']) \
       .assign(LongFlight = lambda x: x['air_time'] > 15.6865) \
       .pipe(csnap, lambda x: x.head(), msg="Added two columns")





#change date format
#.assign(QTR = lambda x: x.QTR.dt.to_period('Q'))
df.groupby(['origin','day'])\
  .agg(
    airtime_avg=pd.NamedAgg(column='air_time',aggfunc='mean'),
    airtime_max=pd.NamedAgg(column='air_time',aggfunc='max'),
    airtime_min=pd.NamedAgg(column='air_time',aggfunc='min'),
    airtime_std=pd.NamedAgg(column='air_time',aggfunc='std'))\
  .reset_index()

df['test'] =1
df.loc[df.index[2],'test'] = 50
df = df.query('air_time > 15.6865') \
       .pipe(csnap,  msg="Before transform") \
       .join(df.groupby(['origin','day'])
               .agg(airtime_avg=pd.NamedAgg(column='test',aggfunc='mean'),
                    airtime_max=pd.NamedAgg(column='air_time',aggfunc='max'),
                    airtime_min=pd.NamedAgg(column='air_time',aggfunc='min'),
                    airtime_std=pd.NamedAgg(column='air_time',aggfunc='std')),on=['origin','day'], how="left")\
       .pipe(csnap,  msg = "After transform")


import pandas as pd
import numpy as np
# Import CSV mtcars
data = pd.read_csv('https://gist.githubusercontent.com/ZeccaLehn/4e06d2575eb9589dbe8c365d61cb056c/raw/64f1660f38ef523b2a1a13be77b002b98665cdfe/mtcars.csv') \
         .rename(columns={'Unnamed: 0':'brand'}) \
         .assign(mpg=lambda x: np.where(x.cyl == 4, -99, x.mpg))





df = pd.DataFrame(np.random.randint(0,100,size=(50000000, 2)), columns=list('AB'))
start_time = time.time()
df2 = df.loc[df.B <50, 'A' ] = -99
print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
df3= df.assign(A=lambda x: np.where(x.B < 50, -99, x.A))
print("--- %s seconds ---" % (time.time() - start_time))





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










