from workflows.AbstractTestRunner import AbstractTestRunner
from utilities.Backtester.backtester import Backtester
from config.Config import Config


class BacktestRunner(AbstractTestRunner):
    def __init__(self, config: Config):
        self.config = config
        self.window_size = config.window_size
        self.estimation_data_list = config.estimation_data_list
        self.backtest_data_list = config.backtest_data_list
        self.strategy_list = config.strategy_list
        self.objective_list = config.objective_list
        self.transaction_cost_bool= config.transaction_cost_bool
        self.transaction_cost_list = config.transaction_cost_list
        self.transaction_cost = config.transaction_cost

    def run(self, df_dict: dict):        
        backtester = Backtester(df_dict, self.estimation_data_list, self.backtest_data_list, 
                                self.window_size, self.strategy_list, self.objective_list,
                                self.transaction_cost_bool, self.transaction_cost_list, 
                                self.transaction_cost)
        backtester.run()



