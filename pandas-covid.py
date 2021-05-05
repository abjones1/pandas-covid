# data source is https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data-with-Ge/n8mc-b4w4

import pandas as pd
import matplotlib.pyplot as plt
from sodapy import Socrata

# Import data into a dataframe with direct pull using socrata.
# Dataset documentation: https://dev.socrata.com/foundry/data.cdc.gov/9mfq-cb36
client = Socrata("data.cdc.gov",
                 "6THglH3n2mVlp2kCZpmOWnhyh",
                 username="abjones1@gmail.com",
                 password="RAWN8di_yur2dirk")
# Results returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("9mfq-cb36", limit=50000)

other_state = input('Enter 2 letter code of comparison state: ')

# Convert to pandas DataFrame
covid_dtypes = {
    'state': 'string',
    'consent_cases': 'string',
    'consent_deaths': 'string'
}
df_covid = pd.DataFrame.from_records(results)

# Convert the date columns to datetime dtype
df_covid[['submission_date', 'created_at']] =\
    df_covid[['submission_date', 'created_at']].apply(pd.to_datetime,
    infer_datetime_format=True)

# Convert the new_case column to int
df_covid['new_case'] = df_covid['new_case'].apply(pd.to_numeric)

# import data into a dataframe from downloaded csv file
# df_covid = pd.read_csv(
#     'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv',
#     dtype=covid_dtypes,
#     parse_dates=['submission_date', 'created_at'],
#     na_values=[""]
#     )

# Create a new df with just Oregon records, sorted by submission_date
df_covid_oregon = df_covid[df_covid['state'] == 'OR'].\
    sort_values(by="submission_date").reset_index(drop=True)

# Create a new df with just Texas records, sorted by submission_date
df_covid_other = df_covid[df_covid['state'] == other_state].\
    sort_values(by="submission_date").reset_index(drop=True)

# Output the latest date in submission_date
print("Last data submission date: {}".format(
    df_covid_oregon['submission_date'].max()))

# Add a column containing the 7 day moving average of new cases,
# implemented with pandas.rolling function
df_covid_oregon['new_cases_7dma'] =\
    df_covid_oregon['new_case'].rolling(7).mean().round()
df_covid_other['new_cases_7dma'] =\
    df_covid_other['new_case'].rolling(7).mean().round()


# Add a column containing the 7 day moving average of new cases,
# implemented with loops. This iterates through the rows by
# index, creating a temporary sum of the 7 rows prior to each index, then
# assigns the value of that temp_sum divided by 7 in the new column.
# for index in range(6, df_covid_oregon_datesorted.shape[0]):
#     temp_sum = 0
#     for row in range(index-6, index+1):
#         temp_sum += df_covid_oregon.loc[row, 'new_case']
#     df_covid_oregon.loc[index, 'new_cases_7dma2'] = round(
#         temp_sum / 7)

plt.figure(figsize=[15, 10])
plt.grid(True)
# plt.plot(df_covid_oregon['submission_date'],
#          df_covid_oregon['new_case'],
#          label='OR daily new COVID cases')
plt.plot(df_covid_oregon['submission_date'],
         df_covid_oregon['new_cases_7dma'],
         label='OR 7-day average of new COVID cases')
plt.plot(df_covid_other['submission_date'],
         df_covid_other['new_cases_7dma'],
         label='{} 7-day average of new COVID cases'.format(other_state))
plt.legend(loc='best')
plt.show()
