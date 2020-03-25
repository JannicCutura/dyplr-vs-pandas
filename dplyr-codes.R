## import libraries and data
library('nycflights13')
df = flights



## some basic overview of the data
head(df)


df %>% group_by(month) %>% summarise(count = n())