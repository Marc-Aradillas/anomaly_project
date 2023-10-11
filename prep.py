import acquire
import pandas as pd

def prep(df, user):
    '''
    The prep function resetos the df by user id andsets index as date column which is changes into a datetime object.
    Pages is also created as a column to count the number of times an endpoint is visited daily as counts.
    '''
    df = df[pd.isnull(df['cohort_id'])]
    df = df[df.user_id == user]
    df.date = pd.to_datetime(df['date'])
    df = df.set_index(df.date)
    pages = df['endpoint'].resample('d').count()
    return pages

def compute_pct_b(pages, span, weight, user):
    '''
    Defined function computes the page count for each day and returns a list of dates with corresponding
    pages, midband, ub,	lb, and	pct_b columns.
    '''
    midband = pages.ewm(span=span).mean()
    stdev = pages.ewm(span=span).std()
    ub = midband + stdev*weight
    lb = midband - stdev*weight
    bb = pd.concat([ub, lb], axis=1)
    my_df = pd.concat([pages, midband, bb], axis=1)
    my_df.columns = ['pages', 'midband', 'ub', 'lb']
    my_df['pct_b'] = (my_df['pages'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def plt_bands(my_df, user):
    '''
    Defined function to plot all bands and display the EMA of accessed number of pages over a year
    '''
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(my_df.index, my_df.pages, label='Number of Pages, User: '+str(user))
    ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
    ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
    ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
    ax.legend(loc='best')
    ax.set_ylabel('Number of Pages')
    plt.show()

def find_anomalies(df, user, span, weight):
    '''
    Defined function used to return a series of users and page counts for each user either specifically or for all users.
    '''
    pages = prep(df, user)
    my_df = compute_pct_b(pages, span, weight, user)
    plt_bands(my_df, user)
    return my_df[my_df.pct_b>1]