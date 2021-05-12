# data source is https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36

import csv
import sqlite3

data_list = []

with open('United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv', newline = '') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        data_list.append(row)

data_headers = data_list[0]
data_list = data_list[1:]

connection = sqlite3.connect("covid.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE us_cases_deaths_by_state (
                    submission_date DATETIME,
                    state TEXT,
                    tot_cases INTEGER,
                    tot_conf_cases INTEGER,
                    tot_prob_cases INTEGER,
                    new_case INTEGER,
                    prob_new_case INTEGER,
                    tot_death INTEGER,
                    tot_conf_death INTEGER,
                    tot_prob_death INTEGER,
                    new_death INTEGER,
                    prob_new_death INTEGER,
                    created_at DATETIME,
                    consent_cases TEXT,
                    consent_deaths TEXT)''')

cursor.executemany('''INSERT INTO us_cases_deaths_by_state VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', data_list)

connection.commit()
cursor.close()
connection.close()
