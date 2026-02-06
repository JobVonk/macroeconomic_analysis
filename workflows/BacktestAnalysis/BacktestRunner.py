from workflows.AbstractTestRunner import AbstractTestRunner
from utilities.Backtester.backtester import Backtester
from config.Config import Config


class BacktestRunner(AbstractTestRunner):
    def __init__(self, config: Config):
        self.config = config
        self.regression_type = config.window_size

    def run(self, df_dict: dict):
        regressor = Backtester(df_dict, self.window_size)
        regressor.run(self.regression_type)



