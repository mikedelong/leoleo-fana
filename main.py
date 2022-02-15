from collections import Counter
from datetime import datetime
from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from matplotlib.pyplot import figure
from matplotlib.pyplot import savefig
from matplotlib.pyplot import scatter
from matplotlib.pyplot import show
from matplotlib.pyplot import style
from pandas import DataFrame
from pandas import read_csv
from seaborn import catplot
from seaborn import countplot


def make_tuple_list(arg):
    return list(zip(arg.index, arg, ))


SHOW = False

if __name__ == '__main__':
    time_start = now()
    logger = getLogger(__name__)
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    logger.info('started.', )
    style.use('fivethirtyeight', )

    # https://github.com/washingtonpost/data-police-shootings
    input_file = 'https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/' \
                 'fatal-police-shootings-data.csv'
    input_df = read_csv(input_file, parse_dates=['date'], )
    logger.info('data shape: {}'.format(input_df.shape, ), )
    logger.info('column names: {} '.format(list(input_df), ), )
    for column in ['armed', 'gender', 'manner_of_death', 'race', 'signs_of_mental_illness', 'state', ]:
        logger.info('{}: {}'.format(column.replace('_', ' '), make_tuple_list(input_df[column].value_counts(), ), ), )
    # add year column
    input_df['year'] = input_df['date'].dt.year
    series = input_df['year'].value_counts().sort_index()
    logger.info(make_tuple_list(series, ), )
    # plot the annualized total for the current year
    current_date = datetime.today()
    current_year = input_df['year'].max()
    past = series[series.index < current_year]
    current = series[current_year]
    scatter(past.index, past)
    # this is a pretty crude approximation to the annualized total
    # todo think about looking at seasonality
    current_annualized = current * 365 // current_date.timetuple().tm_yday
    logger.info('year: {} actual: {} annualized: {} day: {}'.format(current_year, current, current_annualized,
                                                                    current_date.timetuple().tm_yday, ))
    scatter_figure = figure()
    scatter(current_year, current_annualized)
    if SHOW:
        show()
    else:
        savefig('./annual_total.png', )
    del scatter_figure

    count_figure = figure()
    count = countplot(data=input_df[['gender', 'race', 'year', ]], hue='year', x='race', )
    if SHOW:
        show()
    else:
        savefig('./race_year_count.png', )
    del count_figure

    cat_figure = figure()
    cat = catplot(col='gender', data=input_df[['gender', 'race', 'year', ]], hue='year', kind='count', x='race', )
    if SHOW:
        show()
    else:
        savefig('./race_year_catplot.png', )
    del cat_figure

    count_df = DataFrame([(key[0], key[1], key[2], value) for key, value in dict(
        Counter([tuple(item) for item in input_df[['gender', 'race', 'year', ]].to_numpy()])).items()],
                         columns=['gender', 'race', 'year', 'count', ])

    countplot_figure = figure()
    count_plot = countplot(data=count_df, hue='year', x='race', )
    count_plot.legend_.remove()
    if SHOW:
        show()
    else:
        savefig('./race_year_countplot.png', )
    del countplot_figure
    # todo use annualized data for the current year
    current_year = count_df['year'].max()
    day_of_year = current_date.timetuple().tm_yday
    count_df['annualized'] = count_df.apply(
        lambda x: x['count'] if x['year'] < current_year else x['count'] * 365 // day_of_year, axis=1, )
    annualized_df = count_df.drop(['count'], axis=1, )
    annualized_figure = figure()
    annualized_plot = countplot(data=annualized_df, hue='year', x='race', )
    annualized_plot.legend_.remove()
    if SHOW:
        show()
    else:
        savefig('./race_year_annualized_countplot.png', )
    del annualized_figure

    input_df['month'] = input_df['date'].dt.month
    month_counts = input_df[input_df['year'] < current_year]['month'].value_counts().sort_index()
    month_figure = figure()
    month_plot = month_counts.plot(kind='barh', )
    if SHOW:
        show()
    else:
        savefig('./month_barh.png', )
    del month_figure
    logger.info('total time: {:5.2f}s'.format((now() - time_start).total_seconds()))
