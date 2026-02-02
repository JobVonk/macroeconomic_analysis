import pandas as pd
import copy
import numpy as np
from config.Config import Config
import glob


class DataContainer:
    """"
    This Class is a data container that has some support functions to alter the data.
    """
    def __init__(self, config: Config):
        self.data_folder_path = config.data_folder_path
        self.folder_name = config.folder_name
        if config.ecb_fed_bool:
            ecb_raw_df_dict = self.prepare_all_data_in_folder_ecb(self.data_folder_path + 'data_ecb/', self.folder_name)
            fed_raw_df_dict = self.prepare_all_data_in_folder_fed(self.data_folder_path + 'data_fed/', self.folder_name)
            self.raw_df_dict = self.merge_two_dicts(ecb_raw_df_dict, fed_raw_df_dict)
        elif config.ecb_bool:
            self.raw_df_dict = self.prepare_all_data_in_folder_ecb(self.data_folder_path + 'data_ecb/', self.folder_name)
        elif config.fed_bool:
            self.raw_df_dict = self.prepare_all_data_in_folder_fed(self.data_folder_path + 'data_fed/', self.folder_name)

        self.raw_names_df = self.raw_df_dict.keys()
        self.start_date = config.start_date
        self.end_date = config.end_date
        self.frequency_dict = self.find_all_frequencies()
        self.edited_df_dict = self.raw_df_dict
        self.process_dict = config.process_dict

        self.func_dict = {'to_daily': self.to_daily_data, 'to_weekly': self.to_weekly_data,
                          'to_monthly': self.to_monthly_data, 'to_quarterly': self.to_quarterly_data,
                          'to_yearly': self.to_yearly_data, 'relative_returns': self.compute_relative_returns,
                          'clean': self.clean_data, 'compute_change': self.compute_first_order_difference,
                          'division_10': self.division_10, 'division_1m': self.division_1m,
                          'division_1t': self.division_1t, 'minus': self.minus, 'lag_1': self.compute_first_order_lag,
                          'to_first_of_month': self.to_first_of_month, 'lag_3': self.compute_third_order_lag,
                          'lag_6': self.compute_sixt_order_lag, 'lag_12': self.compute_twelfth_order_lag,
                          'time_window': self.select_time_window}

    def run(self):
        self.process_data()

    def filter_all_data_range(self, df_dict: dict) -> dict:
        for name_df in df_dict:
            df_dict[name_df] = df_dict[name_df][(df_dict[name_df]['DATE'] >= self.start_date) &
                                                (df_dict[name_df]['DATE'] <= self.end_date)]
        return df_dict

    def select_time_window(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[(df['DATE'] >= self.start_date) & (df['DATE'] <= self.end_date)]
        return df

    def process_data(self):
        for df in self.process_dict.keys():
            edited_data = self.edited_df_dict[df]
            for process in self.process_dict[df]:
                edited_data = self.func_dict[process](edited_data)
            self.edited_df_dict[df] = edited_data

    def to_daily_data(self, df: pd.DataFrame) -> pd.DataFrame:
        frequency = self.find_frequency(df)
        if frequency == 'W' or frequency == 'M' or frequency == 'Q' or frequency == 'Y':
            df.set_index('DATE', inplace=True)
            df = df.resample('D').mean()
            df = df.interpolate(method='linear')
            df.insert(0, 'DATE', df.index)
            df = df.groupby(df['DATE'].dt.to_period('D')).first()
        else:
            df = df.groupby(df['DATE'].dt.to_period('D')).first()
        df.reset_index(inplace=True, drop=True)
        return df

    def to_weekly_data(self, df: pd.DataFrame) -> pd.DataFrame:
        frequency = self.find_frequency(df)
        if frequency == 'M' or frequency == 'Q' or frequency == 'Y':
            df.set_index('DATE', inplace=True)
            df = df.resample('W').mean()
            df = df.interpolate(method='linear')
            df.insert(0, 'DATE', df.index)
            df = df.groupby(df['DATE'].dt.to_period('W')).first()
        else:
            df = df.groupby(df['DATE'].dt.to_period('W')).first()
        df.reset_index(inplace=True, drop=True)
        return df

    def to_monthly_data(self, df: pd.DataFrame) -> pd.DataFrame:
        frequency = self.find_frequency(df)
        if frequency == 'Q' or frequency == 'Y':
            df.set_index('DATE', inplace=True)
            df = df.resample('ME').mean()
            df = df.interpolate(method='linear')
            df.insert(0, 'DATE', df.index)
            df = df.groupby(df['DATE'].dt.to_period('M')).first()
        else:
            df = df.groupby(df['DATE'].dt.to_period('M')).first()
        df.reset_index(inplace=True, drop=True)
        return df

    def to_quarterly_data(self, df: pd.DataFrame) -> pd.DataFrame:
        frequency = self.find_frequency(df)
        if frequency == 'Y':
            df.set_index('DATE', inplace=True)
            df = df.resample('QE').mean()
            df = df.interpolate(method='linear')
            df.insert(0, 'DATE', df.index)
            df = df.groupby(df['DATE'].dt.to_period('Q')).first()
        else:
            df = df.groupby(df['DATE'].dt.to_period('Q')).first()
        df.reset_index(inplace=True, drop=True)
        return df

    def data_from(self, start_date: str):
        self.edited_data = self.edited_data[self.edited_data['DATE'] >= start_date]

    def data_untill(self, start_date: str):
        self.edited_data = self.edited_data[self.edited_data['DATE'] <= start_date]

    def get_edited_data(self):
        return self.edited_data

    def get_frequency(self):
        return self.frequency

    def deep_copy(self):
        return copy.deepcopy(self)

    def find_all_frequencies(self):
        frequency_dict = {}
        for df in self.raw_df_dict:
            frequency_dict[df] = self.find_frequency(self.raw_df_dict[df])
        return frequency_dict

    @staticmethod
    def compute_first_order_lag(df: pd.DataFrame):
        df.iloc[:, 1] = df.iloc[:, 1].shift(1)
        return df

    @staticmethod
    def compute_third_order_lag(df: pd.DataFrame):
        df.iloc[:, 1] = df.iloc[:, 1].shift(3)
        return df

    @staticmethod
    def compute_sixt_order_lag(df: pd.DataFrame):
        df.iloc[:, 1] = df.iloc[:, 1].shift(6)
        return df

    @staticmethod
    def compute_twelfth_order_lag(df: pd.DataFrame):
        df.iloc[:, 1] = df.iloc[:, 1].shift(12)
        return df

    @staticmethod
    def change_dict_keys(df_dict: dict, new_name_dict: dict):
        new_df_dict = dict((new_name_dict[key], value) for (key, value) in df_dict.items())
        return new_df_dict

    @staticmethod
    def change_column_names(df_dict: list, new_names: dict):
        for df_name in df_dict:
            df = df_dict[df_name]
            df.columns = ['DATE', new_names[df_name]]
            df_dict[df_name] = df
        return df_dict

    @staticmethod
    def to_yearly_data(df: pd.DataFrame) -> pd.DataFrame:
        df = df.groupby(df['DATE'].dt.to_period('Y')).first()
        df.reset_index(inplace=True, drop=True)
        return df

    @staticmethod
    def compute_relative_returns(df: pd.DataFrame) -> pd.DataFrame:
        data = df.iloc[:, 1]
        ret_df = data.diff() / data
        has_nan_or_inf = data.isnull().values.any() or np.isinf(data.values).any()
        if has_nan_or_inf:
            print(f"{df.columns[1]} contains NaN: {has_nan_or_inf}")
        ret_df = pd.DataFrame(ret_df)
        ret_df.insert(0, 'DATE', df['DATE'])
        ret_df.columns = df.columns
        return ret_df

    @staticmethod
    def to_first_of_month(df: pd.DataFrame) -> pd.DataFrame:
        df['DATE'] = df['DATE'].apply(lambda x: x.replace(day=1))
        return df

    @staticmethod
    def compute_first_order_difference(df: pd.DataFrame) -> pd.DataFrame:
        df.iloc[:, 1] = df.iloc[:, 1].diff(1)
        return df

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        df = df[~df.isin([np.nan, np.inf, -np.inf])]
        return df

    @staticmethod
    def division_10(df: pd.DataFrame) -> pd.DataFrame:
        df.iloc[:, 1] = df.iloc[:, 1] / 10
        return df

    @staticmethod
    def division_1m(df: pd.DataFrame) -> pd.DataFrame:
        df.iloc[:, 1] = df.iloc[:, 1] / 1000000.0
        return df

    @staticmethod
    def division_1t(df: pd.DataFrame) -> pd.DataFrame:
        df.iloc[:, 1] = df.iloc[:, 1] / 1000000000000.0
        return df

    @staticmethod
    def minus(df: pd.DataFrame) -> pd.DataFrame:
        df.iloc[:, 1] = -df.iloc[:, 1]
        return df

    @staticmethod
    def filter_dates(max_min_dates: pd.Timestamp, min_max_dates: pd.Timestamp, *args):
        filtered_list = []
        for df in args:
            df = df[df['DATE'] >= max_min_dates]
            df = df[df['DATE'] <= min_max_dates]
            df.iloc[:, 1].reset_index(drop=True)
            filtered_list.append(df)
        return filtered_list

    @staticmethod
    def prepare_all_data_in_folder_fed(data_path: str, folder_name: str):
        files = glob.glob(data_path + folder_name + '*' + '.csv')
        df_dict = {}
        for file in files:
            df = pd.read_csv(file)
            df.rename(columns={'observation_date': 'DATE'}, inplace=True)
            df.DATE = pd.to_datetime(df.DATE, format='%Y-%m-%d')
            df_dict[df.columns[1]] = df
        return df_dict

    @staticmethod
    def prepare_data_fed(data_path: str, file_name: str):
        df = pd.read_csv(data_path + file_name + '.csv')
        df.columns = ['DATE', file_name]
        df.DATE = pd.to_datetime(df.DATE, format='%Y-%m-%d')
        return df

    @staticmethod
    def prepare_all_data_in_folder_ecb(data_path: str, folder_name: str):
        files = glob.glob(data_path + folder_name + '*' + '.csv')
        df_dict = {}
        for file in files:
            df = pd.read_csv(file)
            df.rename(columns={'observation_date': 'DATE'}, inplace=True)
            df.DATE = pd.to_datetime(df.DATE, format='%Y-%m-%d')
            df_dict[df
            ] = df
        return df_dict

    @staticmethod
    def prepare_data_ecb(data_path: str, file_name: str):
        df = pd.read_csv(data_path + file_name + '.csv')
        df = df.iloc[:, [0, 2]]
        df.columns = ['DATE', file_name]
        df.DATE = pd.to_datetime(df.DATE, format='%Y-%m-%d')
        return df

    @staticmethod
    def find_date_range(*args):
        min_dates = []
        max_dates = []
        for arg in args:
            min_dates.append(arg['DATE'].min())
            max_dates.append(arg['DATE'].max())
        max_min_dates = max(min_dates)
        min_max_dates = min(max_dates)
        return max_min_dates, min_max_dates

    @staticmethod
    def merge_two_dicts(x: dict, y: dict) -> dict:
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z

    @staticmethod
    def find_frequency(df: pd.DataFrame) -> str:
        frequency_days = df['DATE'].diff().dt.days
        average = frequency_days.mean()
        round_average = round(average, 1)

        round_average_day = abs(round_average - 1)
        round_average_week = abs(round_average - 7)
        round_average_month = abs(round_average - 31)
        round_average_quarter = abs(round_average - 90)
        round_average_year = abs(round_average - 250)
        min_diff = min([round_average_day, round_average_week, round_average_month, round_average_quarter,
                        round_average_year])
        if min_diff == round_average_day:
            frequency = 'D'
        elif min_diff == round_average_week:
            frequency = 'W'
        elif min_diff == round_average_month:
            frequency = 'M'
        elif min_diff == round_average_quarter:
            frequency = 'Q'
        elif min_diff == round_average_year:
            frequency = 'Y'
        else:
            raise Exception("Date is not daily, weekly monthly or yearly.")
        return frequency


    # def load_data(self) -> dict:
    #     data_dict = {}
    #     for file_name in self.file_names:
    #         data = DataContainer(self.data_folder_path, file_name)
    #         data_dict[file_name + '_ret'] = data
    #         data_dict[file_name + '_price'] = data.deep_copy()
    #     return data_dict


    # @staticmethod
    # def preprocess_data(data: DataContainer, start_date: str, end_date: str, freq: str, returns_bool: bool, lag: int,
    #                     clean_bool: bool = True) -> DataContainer:
    #     data.data_from(start_date)
    #     data.data_untill(end_date)
    #     if freq == 'D':
    #         data.to_daily_data()
    #     elif freq == 'W':
    #         data.to_weekly_data()
    #     elif freq == 'M':
    #         data.to_monthly_data()
    #     elif freq == 'Q':
    #         data.to_quarterly_data()
    #     elif freq == 'Y':
    #         data.to_yearly_data()
    #     else:
    #         raise 'Frequency not found! Choose from: W, M, Q, Y'
    #
    #     if returns_bool:
    #         data.compute_relative_returns()
    #         data.edited_data = pd.DataFrame(data.edited_data)
    #         data.edited_data.insert(0, 'DATE', data.edited_data.index)
    #         data.edited_data['DATE'] = data.edited_data['DATE'].dt.to_timestamp()
    #     if lag > 0:
    #         dates = data.edited_data['DATE']
    #         data.edited_data = data.edited_data.shift(lag)
    #         data.edited_data['DATE'] = dates
    #     if clean_bool:
    #         data.clean_data()
    #
    #     print(f"Frequency {data.edited_data.columns[1]} is: {data.get_frequency()}")
    #     return data.get_edited_data()



