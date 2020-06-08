from logging import INFO
from logging import basicConfig
from logging import getLogger
from time import time
from pandas import read_csv

if __name__ == '__main__':
    time_start = time()
    logger = getLogger(__name__)
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    logger.info('started.', )

    # https://github.com/washingtonpost/data-police-shootings
    input_file = 'https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/' \
                 'fatal-police-shootings-data.csv'
    input_df = read_csv(input_file)
    logger.info(input_df.shape)
    logger.info('total time: {:5.2f}s'.format(time() - time_start))
