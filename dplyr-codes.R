## import libraries and data
library('nycflights13')
library('dplyr')
df = flights



## some basic overview of the data

# show the first 5 rows
head(df)

colnames(df)


df = df %>% 
  mutate(avg_speed = distance/air_time,
         LongFlight = air_time > 150.6865)


df %>%
  group_by(origin) %>%
  summarise(count = n(),
            air_time_avg = mean(air_time, na.rm= TRUE),
            air_time_max = max(air_time, na.rm= TRUE),
            air_time_min = min(air_time, na.rm= TRUE),
            air_time_std = sd(air_time, na.rm= TRUE))


df = df %>%
  group_by(origin) %>%
  mutate(count = n(),
         air_time_avg = mean(air_time, na.rm= TRUE),
         air_time_max = max(air_time, na.rm= TRUE),
         air_time_min = min(air_time, na.rm= TRUE),
         air_time_std = sd(air_time, na.rm= TRUE))


df %>% filter(dep_delay > 3)





