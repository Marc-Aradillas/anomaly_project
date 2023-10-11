import os
import pandas as pd
from env import get_connection

# Constant (to generate filename for csv)
filename = 'curriculum_logs_data.csv'

# Acquire data.
# ----------------------ACQUIRE FUNCTION---------------------------------
def acquire_curlogs():

    '''
    function created to search/retrieve curriculum_logs for codeup exercise and save to csv and return df.
    '''

    if os.path.isfile(filename):
        # If the CSV file exists, read it directly
        return pd.read_csv(filename)
        
    else: 
        query = '''
                SELECT date, path AS endpoint, user_id, cohort_id, ip AS source_ip, name, program_id
                FROM cohorts
                LEFT JOIN logs ON cohorts.id = logs.user_id;
                '''

        url = get_connection('curriculum_logs')
                
        df = pd.read_sql(query, url)

        df['date'] = pd.to_datetime(df['date'])
        
        df.to_csv(filename, index=False)

        return df

#------------------------txt file acquisition----------------------------
colnames = ['date', 'endpoint', 'user_id', 'cohort_id', 'source_ip']

file_name = "anonymized-curriculum-access.txt"

def acquire(file_name):
    # Read the specified file
    df = pd.read_csv(file_name, sep="\s", header=None, names=colnames, usecols=[0, 2, 3, 4, 5])
    
    # Optionally, you can print the first few rows to check the data
    # print(df.head())

    # Return the DataFrame
    return df


# use case for specified file
# Define column names
# colnames = ['date', 'endpoint', 'user_id', 'cohort_id', 'source_ip']

# file_name = "anonymized-curriculum-access.txt"
# df = acquire(file_name)
