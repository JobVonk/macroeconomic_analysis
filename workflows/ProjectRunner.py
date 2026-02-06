from workflows.CreatePlots.CreatePlotRunner import CreatePlotRunner
from workflows.RealEstateAnalysis.RealEstateAnalysisRunner import RealEstateAnalysisRunner
from workflows.DataAnalysis.DataAnalysisRunner import DataAnalysisRunner
from workflows.MacroEconomicAnalysis.MacroEconomicAnalysisRunner import MacroEconomicAnalysisRunner
from workflows.BacktestAnalysis.BacktestRunner import BacktestRunner
from utilities.DataContainer.DataContainer import DataContainer
from config.Config import Config
import pandas as pd
import os


class ProjectRunner:
    def __init__(self, test_name):
        self.test_name = test_name
        self.data_path = r'C:\Users\jjvon\Documents\data'
        self.dict = {'create_plots': CreatePlotRunner, 'real_estate_analysis': RealEstateAnalysisRunner,
                     'data_analysis': DataAnalysisRunner, 'macro_economic_analysis': MacroEconomicAnalysisRunner,
                     'backtester': BacktestRunner}

    def run(self):
        config = Config()
        config.test_parameters()

        data_container = DataContainer(config)
        data_container.run()
        edited_df_dict = data_container.edited_df_dict

        test = self.dict[self.test_name]
        test(config).run(edited_df_dict)

    @staticmethod
    def preprocess_data(config: Config) -> dict:
        df_dict = {}
        path = config.data_folder_path + config.cb_folder + config.folder_name
        for file_name in os.listdir(path):
            df = pd.read_csv(path + file_name)
            df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
            if config.ecb_bool:
                df_dict[file_name[:-4]] = df.iloc[:, [0, 2]]
            elif config.fed_bool:
                df_dict[file_name[:-4]] = df

        for df_name in config.process_dict:
            process_type_list = config.process_dict[df_name]

            for process_type in process_type_list:
                if process_type == 'minus':
                    df_dict[df_name].iloc[:, 1] = -df_dict[df_name].iloc[:, 1]
                elif process_type == 'time_window':
                    df = df_dict[df_name]
                    dates = pd.to_datetime(df.iloc[:, 0])
                    df_dict[df_name] = df[(dates >= config.start_date) & (dates <= config.end_date)]
                elif process_type == 'change':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = df.iloc[:, 1].diff(1)
                    df_dict[df_name] = df
                elif process_type == 'percent_change':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = (df.diff(1).iloc[:, 1] / df.iloc[:, 1]) * 100
                    df_dict[df_name] = df
                elif process_type == 'division_10':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = df_dict[df_name].iloc[:, 1] / 10.0
                    df_dict[df_name] = df
                elif process_type == 'division_100':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = df_dict[df_name].iloc[:, 1] / 100.0
                    df_dict[df_name] = df
                elif process_type == 'division_1M':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = df_dict[df_name].iloc[:, 1] / 100000.0
                    df_dict[df_name] = df
                elif process_type == 'division_1T':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = df_dict[df_name].iloc[:, 1] / 100000000000.0
                    df_dict[df_name] = df
                elif process_type == 'x2':
                    df = df_dict[df_name]
                    df.iloc[:, 1] = df_dict[df_name].iloc[:, 1]
                    df_dict[df_name] = df
        return df_dict

