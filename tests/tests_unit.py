import pandas as pd
from utilities.DataContainer.DataContainer import DataContainer
from utilities.Regressor.Regressor import Regressor
from config.Config import Config
import numpy as np
import logging


class TestsUnit:
    def __init__(self):
        self.config = Config()

        self.daily_dates = ['2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05']
        self.daily_values = [0.05, 0.08, 0.06, 0.11, 0.14]
        self.daily_test_df = pd.DataFrame([self.daily_dates, self.daily_values], index=['DATE', 'VALUE']).T
        self.daily_test_df['DATE'] = pd.to_datetime(self.daily_test_df['DATE'], format='%Y-%m-%d')
        self.daily_test_df['VALUE'] = pd.to_numeric(self.daily_test_df['VALUE'], errors='coerce')

        self.weekly_dates = ['2010-01-01', '2010-01-08', '2010-01-15', '2010-01-22', '2010-01-29', '2010-02-05',
                               '2010-02-12']
        self.weekly_values = [0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03]
        self.weekly_test_df = pd.DataFrame([self.weekly_dates, self.weekly_values], index=['DATE', 'VALUE']).T
        self.weekly_test_df['DATE'] = pd.to_datetime(self.weekly_test_df['DATE'], format='%Y-%m-%d')
        self.weekly_test_df['VALUE'] = pd.to_numeric(self.weekly_test_df['VALUE'], errors='coerce')

        self.monthly_dates = ['2010-01-01', '2010-02-01', '2010-03-01', '2010-04-01', '2010-05-01']
        self.monthly_values = [0.01, 0.02, 0.03, 0.4, 0.5]
        self.monthly_test_df = pd.DataFrame([self.monthly_dates, self.monthly_values], index=['DATE', 'VALUE']).T
        self.monthly_test_df['DATE'] = pd.to_datetime(self.monthly_test_df['DATE'], format='%Y-%m-%d')
        self.monthly_test_df['VALUE'] = pd.to_numeric(self.monthly_test_df['VALUE'], errors='coerce')

        self.quarterly_dates = ['2010-01-01', '2010-04-01', '2010-07-01', '2010-10-01', '2011-01-01']
        self.quarterly_values = [-0.01, -0.02, -0.03, -0.4, -0.5]
        self.quarterly_test_df = pd.DataFrame([self.quarterly_dates, self.quarterly_values], index=['DATE', 'VALUE']).T
        self.quarterly_test_df['DATE'] = pd.to_datetime(self.quarterly_test_df['DATE'], format='%Y-%m-%d')
        self.quarterly_test_df['VALUE'] = pd.to_numeric(self.quarterly_test_df['VALUE'], errors='coerce')

        self.yearly_dates = ['2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01']
        self.yearly_values = [0.01, -0.02, 0.03, -0.4, 0.5]
        self.yearly_test_df = pd.DataFrame([self.yearly_dates, self.yearly_values], index=['DATE', 'VALUE']).T
        self.yearly_test_df['DATE'] = pd.to_datetime(self.yearly_test_df['DATE'], format='%Y-%m-%d')
        self.yearly_test_df['VALUE'] = pd.to_numeric(self.yearly_test_df['VALUE'], errors='coerce')

    def run(self):

        self.tests_unit_data_container()
        self.tests_unit_regressor()

    def tests_unit_regressor(self):
        data_container = DataContainer(self.config)

        lag_df = data_container.compute_first_order_lag(self.monthly_test_df.copy())
        df = self.monthly_test_df.copy()
        df.columns = ['DATE', 'DF']
        lag_df.columns = ['DATE', 'LAG_DF']
        df_dict = {'DF': df, 'LAG_DF': lag_df}

        regressor = Regressor(df_dict, 'DF', ['LAG_DF'])
        self.concat_dfs_unit_test(regressor)
        self.compute_ols_unit_test(regressor)
        self.compute_granger_causality_unit_test(regressor)

    @staticmethod
    def test_unit_concat_dfs(regressor: Regressor):
        concat_df = regressor.concat_dfs(['DF', 'LAG_DF'])
        df = [0.02, 0.03, 0.4, 0.5]
        lag_df = [0.01, 0.02, 0.03, 0.4]
        expected_df = pd.DataFrame([df, lag_df], index=['DF', 'LAG_DF']).T
        expected_df.index = pd.to_datetime(['2010-02-01', '2010-03-01', '2010-04-01', '2010-05-01'])
        assert (expected_df == concat_df).all().all()
        logging.info('concat_dfs_unit_test = Success!')
        return 

    @staticmethod
    def test_unit_compute_ols(regressor: Regressor):
        y = np.array([2, 2, 2, 2, 2]).reshape(5, 1)
        x = np.array([1, 1, 1, 1, 1]).reshape(5, 1)
        df_table = regressor.compute_ols(y, x)

        expected_df = pd.DataFrame(['2.0***',0.00000, 9007199254740992.000, 0.00000], index=['param',
                                                                                                  'std. err.',
                                                                                                  't stat.',
                                                                                                  'p-value']).T
        assert (expected_df.round(6) == df_table.round(6)).all().all()
        logging.info('compute_ols_unit_test = Success!')

    @staticmethod
    def test_unit_compute_granger_causality(regressor: Regressor):
        y = np.array([1, 4, 6, 7, 11, 13, 14, 17]).reshape(8, 1)
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(8, 1)
        df_table = regressor.compute_granger_causality(y, x, max_lag=1)
        expected_df = pd.DataFrame([0.03641, 0.00004, 0.00345, 0.03641, 1.0000],
                                   index=['ssr_ftest', 'ssr_chi2test', 'lrtest', 'params_ftest', 'lag']).T
        assert (expected_df.round(5) == df_table.round(5)).all().all()
        logging.info('compute_granger_causality = Success!')

    def tests_unit_data_container(self):
        data_container = DataContainer(self.config)

        self.find_frequency_unit_test(data_container)

        self.test_unit_lag(data_container)
        self.test_unit_minus(data_container)
        self.test_unit_division10(data_container)
        self.test_unit_division1m(data_container)
        self.test_unit_division1t(data_container)
        self.test_unit_to_daily_data(data_container)
        self.test_unit_to_monthly_data(data_container)
        self.test_unit_to_quarterly_data(data_container)
        self.test_unit_to_yearly_data(data_container)
        self.test_unit_to_first_of_month(data_container)
        self.test_unit_select_time_window(data_container)

        self.test_unit_change(data_container)
        self.test_unit_relative_returns(data_container)

    def test_unit_to_first_of_month(self, data_container: DataContainer):
        weekly_df = data_container.to_first_of_month(self.weekly_test_df)
        weekly_dates = ['2010-01-01', '2010-01-01', '2010-01-01', '2010-01-01', '2010-01-01', '2010-02-01', '2010-02-01']
        weekly_values = [0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03]
        expected_weekly = pd.DataFrame([weekly_dates, weekly_values], index=['DATE', 'VALUE']).T
        expected_weekly['DATE'] = pd.to_datetime(expected_weekly['DATE'], format='%Y-%m-%d')
        assert (weekly_df.iloc[1:, :] == expected_weekly.iloc[1:, :]).all().all()
        logging.info('to_first_of_month_unit_test = Success!')

    def test_unit_lag(self, data_container: DataContainer):
        daily_df = data_container.compute_first_order_lag(self.daily_test_df.copy())
        daily_dates = ['2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05']
        daily_values = [np.nan, 0.05, 0.08, 0.06, 0.11]
        expected_daily = pd.DataFrame([daily_dates, daily_values], index=['DATE', 'VALUE']).T
        expected_daily['DATE'] = pd.to_datetime(expected_daily['DATE'], format='%Y-%m-%d')
        assert (daily_df.iloc[1:, :] == expected_daily.iloc[1:, :]).all().all()
        logging.info('lag_unit_test = Success!')

    def test_unit_minus(self, data_container: DataContainer):
        quarterly_df = data_container.minus(self.quarterly_test_df.copy())
        expected_quarterly_dates = ['2010-01-01', '2010-04-01', '2010-07-01', '2010-10-01', '2011-01-01']
        expected_quarterly_values = [0.01, 0.02, 0.03, 0.4, 0.5]
        expected_quarterly_df = pd.DataFrame([expected_quarterly_dates, expected_quarterly_values], index=['DATE', 'VALUE']).T
        expected_quarterly_df['DATE'] = pd.to_datetime(expected_quarterly_df['DATE'], format='%Y-%m-%d')
        expected_quarterly_df['VALUE'] = pd.to_numeric(expected_quarterly_df['VALUE'], errors='coerce')
        assert (expected_quarterly_df == quarterly_df).all().all()
        logging.info('minus_unit_test = Success!')

    def test_unit_division10(self, data_container: DataContainer):
        quarterly_df = data_container.division_10(self.quarterly_test_df.copy())
        expected_quarterly_dates = ['2010-01-01', '2010-04-01', '2010-07-01', '2010-10-01', '2011-01-01']
        expected_quarterly_values = [-0.001, -0.002, -0.003, -0.04, -0.05]
        expected_quarterly_df = pd.DataFrame([expected_quarterly_dates, expected_quarterly_values], index=['DATE', 'VALUE']).T
        expected_quarterly_df['DATE'] = pd.to_datetime(expected_quarterly_df['DATE'], format='%Y-%m-%d')
        expected_quarterly_df['VALUE'] = pd.to_numeric(expected_quarterly_df['VALUE'], errors='coerce')
        assert (expected_quarterly_df == quarterly_df).all().all()
        logging.info('division10_unit_test = Success!')

    def test_unit_division1m(self, data_container: DataContainer):

        quarterly_df = data_container.division_1m(self.quarterly_test_df.copy())
        expected_quarterly_dates = ['2010-01-01', '2010-04-01', '2010-07-01', '2010-10-01', '2011-01-01']
        expected_quarterly_values = [-0.00000001, -0.00000002, -0.00000003, -0.0000004, -0.0000005]
        expected_quarterly_df = pd.DataFrame([expected_quarterly_dates, expected_quarterly_values], index=['DATE', 'VALUE']).T
        expected_quarterly_df['DATE'] = pd.to_datetime(expected_quarterly_df['DATE'], format='%Y-%m-%d')
        expected_quarterly_df['VALUE'] = pd.to_numeric(expected_quarterly_df['VALUE'], errors='coerce')
        assert (expected_quarterly_df == quarterly_df.round(8)).all().all()
        logging.info('division1m_unit_test = Success!')

    def test_unit_division1t(self, data_container: DataContainer):
        quarterly_df = data_container.division_1t(self.quarterly_test_df.copy())
        expected_quarterly_dates = ['2010-01-01', '2010-04-01', '2010-07-01', '2010-10-01', '2011-01-01']
        expected_quarterly_values = [-0.00000000000001, -0.00000000000002, -0.00000000000003, -0.0000000000004,
                                     -0.0000000000005]
        expected_quarterly_df = pd.DataFrame([expected_quarterly_dates, expected_quarterly_values], index=['DATE', 'VALUE']).T
        expected_quarterly_df['DATE'] = pd.to_datetime(expected_quarterly_df['DATE'], format='%Y-%m-%d')
        expected_quarterly_df['VALUE'] = pd.to_numeric(expected_quarterly_df['VALUE'], errors='coerce')
        assert (expected_quarterly_df == quarterly_df.round(14)).all().all()
        logging.info('division1t_unit_test = Success!')

    def test_unit_change(self, data_container: DataContainer):
        monthly_df = data_container.compute_first_order_difference(self.monthly_test_df.copy())

        monthly_dates = ['2010-01-01', '2010-02-01', '2010-03-01', '2010-04-01', '2010-05-01']
        monthly_values = [np.nan, 0.01, 0.01, 0.37, 0.1]
        expected_monthly = pd.DataFrame([monthly_dates, monthly_values], index=['DATE', 'VALUE']).T
        expected_monthly['DATE'] = pd.to_datetime(expected_monthly['DATE'], format='%Y-%m-%d')
        expected_monthly['VALUE'] = pd.to_numeric(expected_monthly['VALUE'], errors='coerce')
        assert (monthly_df.iloc[1:, :].round(4) == expected_monthly.iloc[1:, :]).all().all()
        logging.info('change_unit_test = Success!')

    def test_unit_relative_returns(self, data_container: DataContainer):
        monthly_df = data_container.compute_relative_returns(self.monthly_test_df.copy())

        monthly_dates = ['2010-01-01', '2010-02-01', '2010-03-01', '2010-04-01', '2010-05-01']
        monthly_values = [np.float64(np.nan), 0.5, 0.3333333333333333, 0.925, 0.2]
        expected_monthly = pd.DataFrame([monthly_dates, monthly_values], index=['DATE', 'VALUE']).T
        expected_monthly['DATE'] = pd.to_datetime(expected_monthly['DATE'], format='%Y-%m-%d')
        expected_monthly['VALUE'] = pd.to_numeric(expected_monthly['VALUE'], errors='coerce')
        assert (monthly_df.iloc[1:, :].round(6) == expected_monthly.iloc[1:, :].round(6)).all().all()
        logging.info('relative_returns_unit_test = Success!')

    def test_unit_find_frequency(self, data_container: DataContainer):
        freq = data_container.find_frequency(self.daily_test_df)
        expected_freq = 'D'
        assert freq == expected_freq

        freq = data_container.find_frequency(self.weekly_test_df)
        expected_freq = 'W'
        assert freq == expected_freq

        freq = data_container.find_frequency(self.monthly_test_df)
        expected_freq = 'M'
        assert freq == expected_freq

        freq = data_container.find_frequency(self.quarterly_test_df)
        expected_freq = 'Q'
        assert freq == expected_freq

        freq = data_container.find_frequency(self.yearly_test_df)
        expected_freq = 'Y'
        assert freq == expected_freq
        logging.info('find_freqency_unit_test = Success!')

    def test_unit_to_daily_data(self, data_container: DataContainer):
        df_daily = data_container.to_daily_data(self.daily_test_df.copy())

        daily_dates = ['2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05']
        daily_values = [0.05, 0.08, 0.06, 0.11, 0.14]
        expected_daily = pd.DataFrame([daily_dates, daily_values], index=['DATE', 'VALUE']).T
        expected_daily['DATE'] = pd.to_datetime(expected_daily['DATE'], format='%Y-%m-%d')
        assert (df_daily == expected_daily).all().all()

        daily_freq = data_container.find_frequency(df_daily)
        assert daily_freq == 'D'

        df_weekly = data_container.to_daily_data(self.weekly_test_df.copy())
        weekly_dates = ['2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05', '2010-01-06',
                        '2010-01-07', '2010-01-08', '2010-01-09', '2010-01-10', '2010-01-11', '2010-01-12',
                        '2010-01-13', '2010-01-14', '2010-01-15', '2010-01-16', '2010-01-17', '2010-01-18',
                        '2010-01-19', '2010-01-20', '2010-01-21', '2010-01-22', '2010-01-23', '2010-01-24',
                        '2010-01-25', '2010-01-26', '2010-01-27', '2010-01-28', '2010-01-29', '2010-01-30',
                        '2010-01-31', '2010-02-01', '2010-02-02', '2010-02-03', '2010-02-04', '2010-02-05',
                        '2010-02-06', '2010-02-07', '2010-02-08', '2010-02-09', '2010-02-10', '2010-02-11',
                        '2010-02-12']
        weekly_values = [0.090000, 0.088571, 0.087143, 0.085714, 0.084286, 0.082857, 0.081429, 0.080000, 0.078571,
                         0.077143, 0.075714, 0.074286, 0.072857, 0.071429, 0.070000, 0.068571, 0.067143, 0.065714,
                         0.064286, 0.062857, 0.061429, 0.060000, 0.058571, 0.057143, 0.055714, 0.054286, 0.052857,
                         0.051429, 0.050000, 0.048571, 0.047143, 0.045714, 0.044286, 0.042857, 0.041429, 0.040000,
                         0.038571, 0.037143, 0.035714, 0.034286, 0.032857, 0.031429, 0.030000]
        expected_weekly = pd.DataFrame([weekly_dates, weekly_values], index=['DATE', 'VALUE']).T
        expected_weekly['DATE'] = pd.to_datetime(expected_weekly['DATE'], format='%Y-%m-%d')
        expected_weekly['VALUE'] = pd.to_numeric(expected_weekly['VALUE'], errors='coerce')

        assert (df_weekly.round(6) == expected_weekly).all().all()

        weekly_freq = data_container.find_frequency(df_weekly)
        assert weekly_freq == 'D'
        logging.info('to_daily_data_unit_test = Success!')

    def test_unit_to_monthly_data(self, data_container: DataContainer):
        df_quarterly = data_container.to_monthly_data(self.quarterly_test_df.copy())

        quarterly_dates = ['2010-01-31', '2010-02-28', '2010-03-31', '2010-04-30', '2010-05-31',
                           '2010-06-30', '2010-07-31', '2010-08-31', '2010-09-30', '2010-10-31',
                           '2010-11-30', '2010-12-31', '2011-01-31']
        quarterly_values = [-0.010000, -0.013333, -0.016667, -0.020000, -0.023333, -0.026667, -0.030000, -0.153333,
                            -0.276667, -0.400000, -0.433333, -0.466667, -0.500000]
        expected_quarterly = pd.DataFrame([quarterly_dates, quarterly_values], index=['DATE', 'VALUE']).T
        expected_quarterly['DATE'] = pd.to_datetime(expected_quarterly['DATE'], format='%Y-%m-%d')
        assert (df_quarterly.round(6) == expected_quarterly).all().all()

        quarterly_freq = data_container.find_frequency(df_quarterly)
        assert quarterly_freq == 'M'

        df_weekly = data_container.to_monthly_data(self.weekly_test_df.copy())
        weekly_dates = ['2010-01-01', '2010-02-05']
        weekly_values = [0.090000, 0.040000]
        expected_weekly = pd.DataFrame([weekly_dates, weekly_values], index=['DATE', 'VALUE']).T
        expected_weekly['DATE'] = pd.to_datetime(expected_weekly['DATE'], format='%Y-%m-%d')
        expected_weekly['VALUE'] = pd.to_numeric(expected_weekly['VALUE'], errors='coerce')

        assert (df_weekly.round(6) == expected_weekly).all().all()

        daily_freq = data_container.find_frequency(df_weekly)
        assert daily_freq == 'M'
        logging.info('to_monthly_data_unit_test = Success!')

    def test_unit_to_quarterly_data(self, data_container: DataContainer):
        df_monthly = data_container.to_quarterly_data(self.monthly_test_df.copy())

        monthly_dates = ['2010-01-01', '2010-04-01']
        monthly_values = [0.010000, 0.4]
        expected_monthly = pd.DataFrame([monthly_dates, monthly_values], index=['DATE', 'VALUE']).T
        expected_monthly['DATE'] = pd.to_datetime(expected_monthly['DATE'], format='%Y-%m-%d')
        assert (df_monthly.round(6) == expected_monthly).all().all()

        quarterly_freq = data_container.find_frequency(df_monthly)
        assert quarterly_freq == 'Q'

        df_yearly = data_container.to_quarterly_data(self.yearly_test_df.copy())
        yearly_dates = ['2010-03-31', '2010-06-30', '2010-09-30', '2010-12-31', '2011-03-31', '2011-06-30', '2011-09-30',
                        '2011-12-31', '2012-03-31', '2012-06-30', '2012-09-30', '2012-12-31', '2013-03-31', '2013-06-30',
                        '2013-09-30', '2013-12-31', '2014-03-31']
        yearly_values = [0.0100, 0.0025, -0.0050, -0.0125, -0.0200, -0.0075, 0.0050, 0.0175, 0.0300, -0.0775, -0.1850,
                         -0.2925, -0.4000, -0.1750, 0.0500, 0.2750, 0.5000]
        expected_yearly = pd.DataFrame([yearly_dates, yearly_values], index=['DATE', 'VALUE']).T
        expected_yearly['DATE'] = pd.to_datetime(expected_yearly['DATE'], format='%Y-%m-%d')
        expected_yearly['VALUE'] = pd.to_numeric(expected_yearly['VALUE'], errors='coerce')

        assert (df_yearly.round(6) == expected_yearly).all().all()

        yearly_freq = data_container.find_frequency(df_yearly)
        assert yearly_freq == 'Q'
        logging.info('to_quarterly_data_unit_test = Success!')

    def test_unit_to_yearly_data(self, data_container: DataContainer):
        df_quarterly = data_container.to_yearly_data(self.quarterly_test_df.copy())

        quarterly_dates = ['2010-01-01', '2011-01-01']
        quarterly_values = [-0.010000, -0.50000]
        expected_quarterly = pd.DataFrame([quarterly_dates, quarterly_values], index=['DATE', 'VALUE']).T
        expected_quarterly['DATE'] = pd.to_datetime(expected_quarterly['DATE'], format='%Y-%m-%d')
        assert (df_quarterly.round(6) == expected_quarterly).all().all()

        quarterly_freq = data_container.find_frequency(df_quarterly)
        assert quarterly_freq == 'Y'
        logging.info('to_yearly_data_unit_test = Success!')

    def test_unit_select_time_window(self, data_container: DataContainer):
        data_container.start_date = pd.Timestamp(year=2012, month=1, day=1)     # end date
        data_container.end_date = pd.Timestamp(year=2013, month=6, day=1)
        df = data_container.select_time_window(self.yearly_test_df)
        dates = ['2012-01-01', '2013-01-01']
        values = [0.03, -0.4]
        expected_df = pd.DataFrame([dates, values], index=['DATE', 'VALUE']).T
        expected_df['DATE'] = pd.to_datetime(expected_df['DATE'], format='%Y-%m-%d')
        expected_df['VALUE'] = pd.to_numeric(expected_df['VALUE'], errors='coerce')
        expected_df.index = [2, 3]
        assert (df == expected_df).all().all()
        logging.info('select_time_window_unit_test = Success!')