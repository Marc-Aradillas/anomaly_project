import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import prep as p


# question 1

def plot_top_five_endpoints(df, title):
    df = df['endpoint'].value_counts().head(5)
    df.plot(kind='bar', figsize=(10, 6), color='turquoise')
    plt.title(title)
    plt.xlabel('File Locations')
    plt.ylabel('Times Visited')
    plt.xticks(rotation=45)
    plt.show()

#ex:

# # Web Development
# df_wd = df[df['endpoint'].str.contains('javascript|css|html|bootstrap|web-design|jquery|mkdocs', case=False)]
# plot_top_five_endpoints(df_wd, 'Top Five Locations Visited (Web Dev)')

# # Cloud Administration
# df_cloud = df[df['endpoint'].str.contains('spring|flask|virtual-enviornments|ajax|php', case=False)]
# plot_top_five_endpoints(df_cloud, 'Top Five Locations Visited (Cloud Administration)')

# # Data Science
# df_ds = df[~df['endpoint'].str.contains('javascript|html|css|spring|java|bootstrap|web-design|jquery|mkdocs/search_index.json|spring|flask|virtual-enviornments|ajax|php|slides/sessions_and_cookies|slides/console_io|slides', case=False, na=False, regex=True)]
# plot_top_five_endpoints(df_ds, 'Top Five Locations Visited (Data Science)')



# question 2

def plot_cohort_endpoint_counts(df, title):
    # Group the data by 'cohort_id' and 'endpoint' and count the number of referrals
    cohort_endpoint_counts = df.groupby(['cohort_id', 'endpoint']).size().reset_index(name='referred_count')

    # Identify the top five lessons referred to across all cohorts
    top_five_endpoints = cohort_endpoint_counts.groupby('endpoint')['referred_count'].sum().nlargest(5)

    # Filter the cohort_endpoint_counts DataFrame to include only the top five endpoints
    filtered_counts = cohort_endpoint_counts[cohort_endpoint_counts['endpoint'].isin(top_five_endpoints.index)]

    # Create a bar plot to visualize cohort referrals to the top five endpoints
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_counts, x='cohort_id', y='referred_count', hue='endpoint')
    plt.title(title)
    plt.xlabel('Cohort ID')
    plt.ylabel('Referred Count')
    plt.xticks(rotation=0)
    plt.legend(title='Endpoint', loc='upper left')
    plt.show()


#ex:

# Web Development
# df_wd = df[df['endpoint'].str.contains('javascript|css|html|bootstrap|web-design|jquery|mkdocs', case=False)]
# plot_cohort_endpoint_counts(df_wd, 'Top Five Endpoints Referred by Cohort (Web Dev)')

# # Cloud Administration
# df_cloud = df[df['endpoint'].str.contains('spring|flask|virtual-enviornments|ajax|php', case=False)]
# plot_cohort_endpoint_counts(df_cloud, 'Top Five Endpoints Referred by Cohort (Cloud)')

# # Data Science
# df_ds = df[~df['endpoint'].str.contains('javascript|html|css|spring|java|bootstrap|web-design|jquery|mkdocs/search_index.json|spring|flask|virtual-enviornments|ajax|php|slides/sessions_and_cookies|slides/console_io|slides', case=False, na=False, regex=True)]
# plot_cohort_endpoint_counts(df_ds, 'Top Five Endpoints Referred by Cohort (Data Science)')


# question 3

def plot_user_activity(user_activity_df, threshold=100):
    # Identify inactive users
    inactive_users = user_activity_df[user_activity_df['endpoint'] < threshold]

    return inactive_users

def plot_num_endpoints(user_ids, num_endpoints, bar_width=0.4):
    x = range(len(user_ids))
    plt.bar(x, num_endpoints, width=bar_width, align='center', label='Number of Endpoints', color='turquoise')
    plt.xticks(x, user_ids)
    plt.xlabel('User ID')
    plt.ylabel('Number of Endpoints')
    plt.title('Number of Endpoints by User ID')
    plt.legend()
    plt.show()

def find_most_visited_endpoint(df, user_ids):
    for user_id in user_ids:
        user_data = df[df['user_id'] == user_id]
        endpoint_counts = user_data['endpoint'].value_counts()
        most_visited_endpoint = endpoint_counts.idxmax()
        count = endpoint_counts.max()
        print(f"User {user_id}: Most visited endpoint is '{most_visited_endpoint}' with {count} visits.")

def plot_most_visited_endpoints(users, endpoints, visit_counts):
    plt.figure(figsize=(10, 6))
    plt.bar(users, visit_counts, color='turquoise')
    plt.xlabel('Users')
    plt.ylabel('Visit Count')
    plt.title('Most Visited Endpoints by User')
    plt.ylim(0, max(visit_counts) + 1)
    for user, endpoint, count in zip(users, endpoints, visit_counts):
        plt.text(user, count + 0.2, f'{endpoint}\n({count} visits)', ha='center', fontsize=9)
    plt.show()

# ex:

# # First cell
# user_activity_df = df.groupby('user_id')['endpoint'].count().reset_index()
# inactive_users = plot_user_activity(user_activity_df)

# # Second cell (no function needed, it's just a filter)

# # Third cell
# user_ids = [13, 24, 55]
# num_endpoints = [92, 24, 88]
# plot_num_endpoints(user_ids, num_endpoints)

# # Fourth cell
# user_ids = [13, 24, 55]
# find_most_visited_endpoint(df, user_ids)

# # Fifth cell
# users = ['User 13', 'User 24', 'User 55']
# endpoints = ['javascript-i/functions', 'mkdocs/search_index.json', 'spring/fundamentals/security/authentication']
# visit_counts = [12, 3, 9]
# plot_most_visited_endpoints(users, endpoints, visit_counts)
# This code defines functions to handle each task, making it more modular and reusable. You can then call these functions as needed for your analysis.


# question 4

def plot_pages_over_time(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(df.date)
    pages = df['endpoint'].resample('d').count()
    plt.plot(pages)
    plt.show()

def find_anomalies(df, span, weight):
    span = 30
    weight = 3.5
    # here we are looping through all user ids
    anomalies = pd.DataFrame()
    for u in list(df.user_id.unique()):
        user_df = p.find_anomalies(df, u, span, weight)
        anomalies = pd.concat([anomalies, user_df], axis=0)

# def plot_top_ip_addresses(df, num_top_ips=5):
#     ip_df = df['source_ip'].value_counts()
#     ip_df['count'].sort_values().tail(num_top_ips).plot.barh(figsize=(5, 9))
#     plt.title('Number of Unique IP Addresses')
#     plt.show()

def get_user_tagged_ip(df, threshold_low=0.5, threshold_high=1.0):
    user_tagged_ip = (
        df.groupby('source_ip')
        .user_id.value_counts(normalize=True)
        .rename('freq_user_tagged_ip')
        .reset_index()
    )
    return user_tagged_ip[(user_tagged_ip['freq_user_tagged_ip'] > threshold_low) & (user_tagged_ip['freq_user_tagged_ip'] < threshold_high)]

# ex:


# # Plot pages over time
# plot_pages_over_time(df)

# # Analyze anomalies using your 'find_anomalies' function

# # Plot top IP addresses
# plot_top_ip_addresses(df)

# # Get user-tagged IP addresses
# user_tagged_ip = get_user_tagged_ip(df)



# question 5

def preprocess_data(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(df.date)
    return df

def filter_data_by_year(df, year):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

def plot_daily_observations(df, program_id, title):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    daily_counts = df[df['program_id'] == program_id].resample('D').count()
    plt.figure(figsize=(12, 6))
    daily_counts['program_id'].plot()
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Number of Observations')
    plt.grid(True)
    plt.show()

def add_suffix_to_column(df, column_name, suffix):
    df[column_name] = df[column_name].apply(lambda x: x + suffix)
    return df

# ex:
# # Cell 1
# df = preprocess_data(df)

# # Cell 2
# dates_in_2018 = filter_data_by_year(df, 2018)
# dates_in_2019 = filter_data_by_year(df, 2019)
# dates_in_2020 = filter_data_by_year(df, 2020)

# # Cell 3
# df_2019 = filter_data_by_year(df, 2019)
# plot_daily_observations(df_2019, 2, 'Daily Observations in 2019')

# # Cell 4
# df_2018 = filter_data_by_year(df, 2018)
# plot_daily_observations(df_2018, 1, 'Daily Observations in 2018')

# # Cell 5
# datascience_df = df[~df['endpoint'].str.contains('javascript|html|css|spring|java|bootstrap|web-design|jquery|mkdocs|search_index.json|spring|flask|virtual-enviornments|ajax|php|slides/sessions_and_cookies|slides/console_io|slides', case=False, na=False, regex=True)]
# webdev_df = df[df['endpoint'].str.contains('javascript|css|html|bootstrap|web-design|jquery|mkdocs|search_index.json|spring|flask|virtual-enviornments|ajax|php|slides/sessions_and_cookies|slides/console_io|slides', case=False, na=False, regex=True)]

# # Cell 6
# datascience_df = add_suffix_to_column(datascience_df, 'endpoint', ' (ds)')
# webdev_df = add_suffix_to_column(webdev_df, 'endpoint', ' (web)')

# # Cell 7
# df_2018 = filter_data_by_year(datascience_df, 2018)
# plot_daily_observations(df_2018, 2, 'Daily Observations in 2018 for Program ID 2')

# # Cell 8
# df_2019 = filter_data_by_year(datascience_df, 2019)
# plot_daily_observations(df_2019, 1, 'Daily Observations in 2019 for Program ID 1')

# # Cell 9
# df_2018 = filter_data_by_year(webdev_df, 2018)
# plot_daily_observations(df_2018, 3, 'Daily Observations in 2018 for Web Dev Students (Program ID 3)')

