from utilities.DataContainer.DataContainer import DataContainer
import pandas as pd
import numpy as np


class Backtester:
    def __init__(self, df_dict: dict, estimation_data_list: list[str], backtest_data_list: list[str], 
                 window_size: int, strategy_list: str, objective_list: list[str], transaction_cost_bool: bool, 
                 transaction_cost_list: list, transaction_cost: float):
        self.df_dict = df_dict
        self.estimation_data_list = estimation_data_list
        self.backtest_data_list = backtest_data_list
        self.window_size = window_size
        self.strategies_dict = {'mean_strat': self.mean_strat}
        self.strategy_list = strategy_list

        self.objective_dict = {'obj_sum': self.obj_sum}
        self.objective_list = objective_list


        self.transaction_cost_bool = transaction_cost_bool
        self.transanction_cost_list = transaction_cost_list
        self.transaction_cost_dict = {'proportional_cost': self.proportional_transaction_cost}
        self.transaction_cost = transaction_cost 


    def run(self):
        
        estimation_data = self.estimation_data_list[0] 
        estimation_df = self.df_dict[estimation_data]
        estimation_df = estimation_df.set_index('DATE', inplace=False)
    
        backtest_data = self.backtest_data_list[0]
        backtest_df = self.df_dict[backtest_data]
        backtest_df = backtest_df.set_index('DATE', inplace=False)

        strategy = self.strategy_list[0]
        strat_func = self.strategies_dict[strategy]

        strat_deltas = estimation_df.rolling(window=self.window_size).apply(strat_func, raw=True)
        
        objective = self.objective_list[0]
        trade_profit, cum_trade_profits = self.objective_dict[objective](strat_deltas, backtest_df)
        
        if self.transaction_cost_bool:
            transaction_cost_func = self.transanction_cost_list[0]
            cost, cum_cost = self.transaction_cost_dict[transaction_cost_func](strat_deltas, self.transaction_cost)

        net_profit = trade_profit - cost
        net_cum_profits = cum_trade_profits - cum_cost
        
    
    @staticmethod
    def obj_sum(strat_deltas: pd.DataFrame, backtest_df: pd.DataFrame) -> tuple[pd.DataFrame]:
        profits = strat_deltas * backtest_df.diff(1).shift(-1)
        obj = np.sum(profits)
        cum_df = profits.cumsum()
        return obj, cum_df

    @staticmethod
    def mean_strat(window_values: np.array) -> float:
        avg = np.mean(window_values)
        recent_price = window_values[-1]
        if recent_price < avg:
            delta = 1.0 
        else:
            delta = 0.0
        return delta

    @staticmethod
    def proportional_transaction_cost(strat_deltas: pd.DataFrame, proportional_cost: float) -> pd.DataFrame:
        cost_df = proportional_cost * strat_deltas.diff(1)
        total_cost = np.sum(abs(cost_df))
        cum_cost = abs(cost_df).cumsum()
        return total_cost, cum_cost




        

        

