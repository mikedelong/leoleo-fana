from logging import INFO
from logging import basicConfig
from logging import getLogger
from time import time

from matplotlib.pyplot import scatter
from matplotlib.pyplot import show
from matplotlib.pyplot import subplots
from pandas import read_csv
from datetime import datetime

if __name__ == '__main__':
    time_start = time()
    logger = getLogger(__name__)
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    logger.info('started.', )

    # https://github.com/washingtonpost/data-police-shootings
    input_file = 'https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/' \
                 'fatal-police-shootings-data.csv'
    input_df = read_csv(input_file, parse_dates=['date'], )
    logger.info(input_df.shape)
    logger.info(list(input_df))
    logger.info('gender: {}'.format(input_df['gender'].value_counts()))
    logger.info('race: {}'.format(input_df['race'].value_counts()))
    # add year column
    input_df['year'] = input_df['date'].dt.year

    series = input_df['year'].value_counts().sort_index()
    logger.info(series)
    # scatter(series.index, series)
    figure, axes = subplots()
    # plot the annualized total for the current year
    current_date = datetime.today()
    current_year = current_date.year
    past = series[series.index < current_year]
    current = series[current_year]
    scatter(past.index, past)
    current_annualized = current * 365 // current_date.timetuple().tm_yday
    logger.info('year: {} actual: {} annualized: {} day: {}'.format(current_year, current, current_annualized,
                                                                    current_date.timetuple().tm_yday, ))
    scatter(current_year, current_annualized)
    show()

    logger.info('total time: {:5.2f}s'.format(time() - time_start))
