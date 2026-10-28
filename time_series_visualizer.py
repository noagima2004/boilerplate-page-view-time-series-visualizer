import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_date=['date'], index_col='date')
#parse_dates=['date'] converts the date column (text in the CSV doc) into objects of type
#real date (datetime64), this allows to extract years, months or days
#index_col='date' assigns date as the index of DataFrame



# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))
    #fig is the whole figure, ax is the specific drawing area (the grid part)
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    #df.index are the dates, for X axis, and df['value'] are number of visits, for Y axis

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df_copy() #just to not permanently modify the DF
    df_bar['year'] = df_bar.index.year #.year extracts the year as a whole number
    df_bar['month'] = df_bar.index.strftime('%B') #strftime('%B') extracts the whole number of the month in english

    # Draw bar plot
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    #unstack() gets the 2nd index level (month) and transform into columns, so the data are converted into a double-input
    #table where rows are years and columns are months

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar= df_bar.reindex(columns=month_order) #so months don't get alphabetically ordered

    fig=df_bar.plot(kind='bar', figsize=(9,7)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legent(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True) #date converted again in a normal column
    df_box['year'] = [d.year for d in df_box.date] #d.year extracts the numeric year,
    # and d.strftime('%b') extracts the abreviation of 3 letterss in english
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2, figsize=(20,7))
    # subplots(1,2, ...) means 1 row, 2 columns

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], palette='tab10')
    #axes[0] is the left plto and axes[1] is the right one

    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='year', y='value', data=df_box, order=month_order, ax=axes[1], palette='tab10')

    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
