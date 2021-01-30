
## import libraries
import numpy as np
import pandas as pd
import time
from nycflights13 import flights

print("This is pandas version {}. Make sure your version is >0.25 ".format(pd.__version__))

## useful functions
def csnap(df, fn=lambda x: x.shape, msg=None):
    """ Custom Help function to print things in method chaining.
        Returns back the df to further use in chaining.
        Credits: https://towardsdatascience.com/the-unreasonable-effectiveness-of-method-chaining-in-pandas-15c2109e3c69
    """
    if msg:
        print(msg)
    display(fn(df))
    return df


def reorder(df, cols):
    """Reorders the dataframe df by taking the provided columns first and then
    puts the remaining columns

    Parameters:
        df (panda dataframe): A panda dataframe which columns should be reordered
        cols (list): a list vontaining the names of the columns that should be first
        """
    others = df.columns.difference(cols).tolist()
    return df[cols+others]



df = flights



# some stats and info
df.head()





## add / replace variables
df = df.assign(sched_arr_time2 =lambda x:  x.sched_arr_time**2,
               sched_arr_time = lambda x: x.sched_arr_time.fillna(0),
               dep_time=lambda x: np.where(x.arr_delay < 0, -99, x.dep_time),
               LongFlight=lambda x: x['air_time'] > 15.6865)

## order variables
df = df.pipe(reorder, ['year', 'month', 'day','dep_delay'])

## rename columns
df = df.rename({'time_hour': 'timehour'}, axis='columns')

## show duplicates
df[df.tailnum.duplicated(keep=False)].sort_values(['year', 'month', 'day'])

## case-when
df['length'] = np.where((df["distance"].between(0, 500, inclusive=False) and (df.dep_delay < 100 ), 'Short',
               np.where(df['distance'].between(500, 1500, inclusive=False), 'Medium',
               np.where(df['distance'].between(1500, df['distance'].max(), inclusive=False), 'Long',
                            'Unknown')))


## groupby by summarise
df.groupby(['origin', 'day']) \
    .agg(
    airtime_avg=pd.NamedAgg(column='air_time', aggfunc='mean'),
    airtime_max=pd.NamedAgg(column='air_time', aggfunc='max'),
    airtime_min=pd.NamedAgg(column='air_time', aggfunc='min'),
    airtime_std=pd.NamedAgg(column='air_time', aggfunc='std')) \
    .reset_index()



## groupby mutate
df = df.query('air_time > 15.6865') \
    .pipe(csnap, msg="Before transform") \
    .join(df.groupby(['origin', 'day'])
          .agg(airtime_avg=pd.NamedAgg(column='air_time', aggfunc='mean'),
               airtime_max=pd.NamedAgg(column='air_time', aggfunc='max'),
               airtime_min=pd.NamedAgg(column='air_time', aggfunc='min'),
               airtime_std=pd.NamedAgg(column='air_time', aggfunc='std'),
               count_connections=pd.NamedAgg(column='air_time', aggfunc='count'),
               count_connections2=pd.NamedAgg(column='air_time', aggfunc='size')
               ), on=['origin', 'day'], how="left") \
    .pipe(csnap, msg="After transform")



# or with assign
df.assign(newID = df.groupby(['origin']).ngroup(),
          min_airtime = df.groupby(['origin','day'])['air_time'].transform('min'),
          count_connections = df.groupby(['origin','dest'])['air_time'].transform('count'))

# same thing but without NamedAgg
df['min_airtime'] = df.groupby(['origin','day'])['air_time'].transform('min')
df['max_airtime'] = df.groupby(['origin','day'])['air_time'].transform('max')
df['std_airtime'] = df.groupby(['origin','day'])['air_time'].transform('std')
df['count_connections'] = df.groupby(['origin','dest'])['max_airtime'].transform('count')




## working with dates and time



## working with date
df = df.assign(date = lambda x: pd.to_datetime(x[['year','month', 'day']]))



df = df.assign(qtr = lambda x: x.date.dt.to_period('q'))




## filter
df4 = df.query("dep_delay > 0 and \
               arr_delay.notnull() \
               and carrier.str.contains('U') and \
               tailnum.str.len() == 5 and \
               qtr > @pd.Period('2013Q1','Q') ", engine='python')



## other
import pandas as pd
import numpy as np

# Import CSV mtcars
data = pd.read_csv(
    'https://gist.githubusercontent.com/ZeccaLehn/4e06d2575eb9589dbe8c365d61cb056c/raw/64f1660f38ef523b2a1a13be77b002b98665cdfe/mtcars.csv') \
    .rename(columns={'Unnamed: 0': 'brand'}) \
    .assign(mpg=lambda x: np.where(x.cyl == 4, -99, x.mpg))

df = pd.DataFrame(np.random.randint(0, 100, size=(50000000, 2)), columns=list('AB'))
start_time = time.time()
df2 = df.loc[df.B < 50, 'A'] = -99
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
df3 = df.assign(A=lambda x: np.where(x.B < 50, -99, x.A))
print("--- %s seconds ---" % (time.time() - start_time))


import plotly.graph_objects as go


fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ["relative", "relative", "total", "relative", "relative", "total"],
    x = ["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
    textposition = "outside",
    text = ["+60", "+80", "", "-40", "-20", "Total"],
    y = [60, 80, 0, -40, -20, 0],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
        title = "Profit and loss statement 2018",
        showlegend = True
)

fig.show()
fig.write_image("fig1.jpeg", scale=3)



fig = go.Figure(go.Waterfall(
    x = [["2016", "2017", "2017", "2017", "2017", "2018", "2018", "2018", "2018"],
       ["initial", "q1", "q2", "q3", "total", "q1", "q2", "q3", "total"]],
    measure = ["absolute", "relative", "relative", "relative", "total", "relative", "relative", "relative", "total"],
    y = [10, 20, 30, -10, None, 10, 20, -40, None], base = 300,
    decreasing = {"marker":{"color":"#FF4B00", "line":{"color":"#FF4B00", "width":2}}},
    increasing = {"marker":{"color":"#65B800"}},
    totals = {"marker":{"color":"#003299", "line":{"color":"#003299", "width":3}}}
))

fig.update_layout(title = "Profit and loss statement", waterfallgap = 0.3)

fig.show()





