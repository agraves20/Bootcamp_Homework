import pandas as pd
import os
import csv

datafile_csv = os.path.join('employee_data1.csv')
datafile2_csv = os.path.join('employee_data2.csv')

datafile_df = pd.read_csv(datafile_csv)
datafile2_df = pd.read_csv(datafile2_csv)

combined_datafile_df = datafile_df.append(datafile2_df)

combined_datafile_df[['First Name','Last Name']] = combined_datafile_df['Name'].str.split(expand=True)

del combined_datafile_df['Name']

combined_datafile_df = combined_datafile_df[['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State']]

combined_datafile_df['DOB'] = pd.to_datetime(combined_datafile_df.DOB).dt.strftime('%m/%d/%Y')

combined_datafile_df['SSN'] = "***-**-" + combined_datafile_df['SSN'].str[7:11]

combined_datafile_df['State'] = combined_datafile_df['State'].replace({
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
})
print(combined_datafile_df)

combined_datafile_df.to_csv("combined_final.csv", encoding="utf-8", index=False, header=True)