from datetime import datetime
from logging import INFO
from logging import basicConfig
from logging import getLogger
from time import time

from matplotlib.pyplot import savefig
from matplotlib.pyplot import scatter
from matplotlib.pyplot import show
from matplotlib.pyplot import style
from matplotlib.pyplot import subplots
from pandas import read_csv
from seaborn import catplot
from seaborn import countplot


def make_tuple_list(arg):
    return list(zip(arg.index, arg, ))


if __name__ == '__main__':
    time_start = time()
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
    figure, axes = subplots()
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
    scatter(current_year, current_annualized)
    do_show = False
    if do_show:
        show()
    else:
        savefig('./annual_total.png', )

    count = countplot(data=input_df[['gender', 'race', 'year', ]], hue='year', x='race', )
    if do_show:
        show()
    else:
        savefig('./race_year_count.png', )

    cat = catplot(col='gender', data=input_df[['gender', 'race', 'year', ]], hue='year', kind='count', x='race', )
    if do_show:
        show()
    else:
        savefig('./race_year_cat.png', )

    # todo build a summary table with annualized data for the current year

    logger.info('total time: {:5.2f}s'.format(time() - time_start))
