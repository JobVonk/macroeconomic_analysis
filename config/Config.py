from dataclasses import dataclass
import pandas as pd


@dataclass
class Config:
    def __init__(self):
        self.start_date = pd.Timestamp(year=2000, month=1, day=1)     # end date
        self.end_date = pd.Timestamp(year=2016, month=1, day=1)       # start date
        self.freq = 'M'                    # frequency of the data, either daily (D), weekly (W), monthly (M),
                                           # quarterly (Q), or yearly (Y)
        self.returns_bool = False          # specify if data has to be in terms of returns
        self.lag = 0                       # specify a if data has to be lagged
        self.clean_bool = True             # If true data is cleaned from possible inf or nan values
        self.data_folder_path = "C:/Users/jjvon/Documents/visual code/macro_economic_analysis/data/"
        self.output_path = self.data_folder_path + '../../results/macro_economic_anlaysis/'

        self.ecb_fed_bool = False
        self.plot_type = 'line'

        # ----------------------- backtester params -----------------------
        
        self.window_size = 3
        self.estimation_data_list = ['CPIAUCSL_PC1', 'CPILFESL_PC1', 'UNRATE']
        self.backtest_data_list = ['CPIAUCSL_PC1', 'CPILFESL_PC1', 'UNRATE']
        self.strategy_list = ['mean_strat']
        self.objective_list = ['obj_sum']
        self.transaction_cost_bool = True
        self.transaction_cost_list = ['proportional_cost']    
        self.transaction_cost = 0.01

        # ----------------------- regression params ----------------------- 

        self.ecb_bool = False
        self.fed_bool = True
        self.folder_name = 'regression_jp/'

        self.ecb_bool = False
        self.fed_bool = True
        self.folder_name = 'unemployement_us/'
        self.plot_title = 'Unemployment rate vs % change in CPI for U.S.'
        files = ['CPIAUCSL_PC1', 'CPILFESL_PC1', 'UNRATE']
        self.plot_legend_names = {files[0]: '% Change CPI: for All Urban Consumers: All items in U.S. City Average',
                                  files[1]: '% Change CPI for All Urban Consumers: All Items Less Food and Energy in U.S. '
                                            'City Average',
                                  files[2]: 'Unemployment Rate'}
        self.plot_colors = {files[0]: 'blue', files[1]: 'darkblue', files[2]: 'red'}
        self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'dashed',
                                     files[2]: 'solid'}

        self.process_dict = {files[0]: [], files[1]: [],
                             files[2]: []}

        self.ymin = -5
        self.ymax = 25
        self.ylabel = 'percentage'


        # self.y_var = 'FPCPITOTLZGJPN'
        # self.x_vars_list = ['DEBTTLJPA188A_PC1', 'MYAGM2JPM189S_PC1', 'IRSTCB01JPM156N']
        # files = ['FPCPITOTLZGJPN', 'DEBTTLJPA188A_PC1', 'MYAGM2JPM189S_PC1', 'IRSTCB01JPM156N']
        # # self.x_vars_list = ['DEBTTLJPA188A_PC1', 'MYAGM2JPM189S_PC1', 'IRSTCB01JPM156N']
        # files = ['FPCPITOTLZGJPN', 'DEBTTLJPA188A_PC1', 'MYAGM2JPM189S_PC1', 'IRSTCB01JPM156N']
        #
        self.regression_type = 'var'

        # self.process_dict = {files[0]: ['to_monthly', 'to_first_of_month', 'time_window'],
        #                      files[1]: ['to_monthly', 'to_first_of_month', 'time_window']
        #                      }

        #
        # self.folder_name = 'regression_us/'
        #
        self.y_var = 'CPILFESL_PC1'
        self.x_vars_list = ['DCOILBRENTEU', 'FEDFUNDS', 'GFDEBTN_PC1', 'GFDEGDQ188S_PCH', 'MYAGM2USM052S_PC1']
        # files = ['CPIAUCSL_PC1', 'DCOILBRENTEU', 'FEDFUNDS', 'GFDEBTN_PC1', 'GFDEGDQ188S_PCH', 'MYAGM2USM052S_PC1']
        #
        # self.regression_type = 'var'
        #
        # self.process_dict = {files[0]: ['to_monthly', 'to_first_of_month', 'time_window'],
        #                      files[1]: ['to_monthly', 'to_first_of_month', 'time_window'],
        #                      files[2]: ['to_monthly', 'to_first_of_month', 'time_window'],
        #                      files[3]: ['to_monthly', 'to_first_of_month', 'time_window'],
        #                      files[4]: ['to_monthly', 'to_first_of_month', 'time_window'],
        #                      files[5]: ['to_monthly', 'to_first_of_month', 'time_window']}

        # ------------------------- plot params --------------------
        # self.process_dict = {files[0]: ['to_monthly'], files[1]: ['to_monthly'],
        #                      files[2]: ['to_monthly']}
        # self.ecb_bool = True
        # self.fed_bool = False
        # self.folder_name = 'ecb_hicp_gdp/'
        # self.plot_title = 'Change in government spending vs Change in HICP for EU'
        # files = ['ECB Data Portal_HICP', 'ECB Data Portal_SECMON', 'ECB Data Portal_DEBTGDP',
        #          'ECB Data Portal_DEBTGDP - kopie', 'ECB Data Portal_M2']
        # self.plot_legend_names = {files[0]: 'HICP Overall index, Euro area (changing composition)',
        #                           files[1]: '% Change Securities held for monetary policy purposes - ECB',
        #                           files[2]: 'Change Government debt (consolidated) (as % of GDP), '
        #                                     'Euro area 20 (fixed composition)',
        #                           files[3]: '% Change Government debt (consolidated) (as % of GDP), '
        #                                     'Euro area 20 (fixed composition)',
        #                           files[4]: '% Change Monetary aggregate M2 Euro area (changing composition)'
        #                           }
        # # reported by MFIs, central gov. and post office giro '
        # #'institutions in the euro area (stocks),
        # self.plot_colors = {files[0]: 'blue', files[1]: 'green', files[2]: 'red', files[3]: 'darkred',
        #                     files[4]: 'brown'}
        # self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'solid',
        #                              files[2]: 'solid', files[3]: 'dashed', files[4]: 'dotted'}
        #
        # self.process_dict = {files[0]: ['time_window'], files[1]: ['time_window', 'percent_change'],
        #                      files[2]: ['time_window', 'change'], files[3]: ['time_window', 'percent_change'],
        #                      files[4]: ['time_window', 'percent_change']}
        #
        # self.ymin = -5
        # self.ymax = 15
        # self.ylabel = 'percentage/value'
        #
        # self.ecb_bool = False
        # self.fed_bool = True
        # self.folder_name = 'jp_deficit_spending_inflation/'
        # self.plot_title = 'Change in Government Spending vs Change in CPI for Japan'
        # files = ['FPCPITOTLZGJPN', 'DEBTTLJPA188A_PC1', 'DEBTTLJPA188A_CH1', 'MYAGM2JPM189S_PC1', 'IRSTCB01JPM156N']
        # self.plot_legend_names = {files[0]: 'Inflation, consumer prices for Japan',
        #                           files[1]: '% Change Central government debt, total (% of GDP) for Japan',
        #                           files[2]: 'Change Central government debt, total (% of GDP) for Japan',
        #                           files[3]: '% Change M2 for Japan',
        #                           files[4]: 'Interest rates: Immediate Interbank Rates (< 24 Hours) Total for for Japan'}
        # self.plot_colors = {files[0]: 'blue', files[1]: 'red', files[2]: 'darkred', files[3]: 'brown', files[4]: 'green'}
        # self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'solid',
        #                              files[2]: 'dashed', files[3]: 'dotted', files[4]: 'solid'}
        #
        # self.process_dict = {files[0]: ['time_window'], files[1]: ['time_window'],
        #                      files[2]: ['time_window'], files[3]: ['time_window'], files[4]: ['time_window']}
        #
        # self.ymin = -5
        # self.ymax = 25
        # self.ylabel = 'percentage/value'

        # self.ecb_bool = False
        # self.fed_bool = True
        # self.folder_name = 'us_deficit_spending_inflation_ch1/'
        #
        # self.plot_title = 'Change in Federal Spending vs Change in CPI for US'
        # files = ['CPIAUCSL_CH1', 'CPILFESL_CH1', 'FYFSD', 'GFDEBTN_CH1', 'GFDEGDQ188S_CH1', 'MYAGM2USM052S_CH1']
        #
        # self.plot_legend_names = {files[0]: 'Change CPI: for All Urban Consumers: All items in U.S. City Average',
        #                           files[1]: 'Change CPI for All Urban Consumers: All Items Less Food and Energy in U.S. '
        #                                     'City Average',
        #                           files[2]: 'Minus Change Federal Surplus or Deficit / 1M',
        #                           files[3]: 'Change Federal Debt: Total Public Debt / 1M',
        #                           files[4]: 'Change Federal Debt: Total Public Debt as Percent of GDP',
        #                           files[5]: 'Change M2 for United States / 1T'}
        # self.plot_colors = {files[0]: 'blue', files[1]: 'darkblue', files[2]: 'red', files[3]: 'darkred',
        #                     files[4]: 'orange', files[5]: 'brown'}
        # self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'dotted',
        #                              files[2]: 'solid', files[3]: 'dashed', files[4]: 'solid', files[5]: 'dotted'}
        #
        # self.process_dict = {files[0]: ['time_window'], files[1]: ['time_window'],
        #                      files[2]: ['time_window', 'division_1M', 'minus'],
        #                      files[3]: ['time_window', 'division_1M'], files[4]: ['time_window'],
        #                      files[5]: ['time_window', 'division_1T']}
        # self.ymin = -12
        # self.ymax = 50
        # self.ylabel = 'value'

        # self.ecb_bool = False
        # self.fed_bool = True
        # self.folder_name = 'us_deficit_spending_inflation_pc1/'
        # self.plot_title = '% Change in Federal Spending vs % Change in CPI for US'
        # files = ['CPIAUCSL_PC1', 'CPILFESL_PC1', 'FYFSD_PC1', 'GFDEBTN_PC1', 'GFDEGDQ188S_PCH', 'MYAGM2USM052S_PC1']
        # self.plot_legend_names = {files[0]: '% Change CPI: for All Urban Consumers: All items in U.S. City Average',
        #                           files[1]: '% Change CPI for All Urban Consumers: All Items Less Food and Energy in U.S. '
        #                                     'City Average',
        #                           files[2]: '% Change Federal Surplus or Deficit / 10',
        #                           files[3]: '% Change Federal Debt: Total Public Debt',
        #                           files[4]: '% Change Federal Debt: Total Public Debt as Percent of GDP',
        #                           files[5]: '% Change M2 for United States'}
        # self.plot_colors = {files[0]: 'blue', files[1]: 'darkblue', files[2]: 'red', files[3]: 'darkred',
        #                     files[4]: 'orange',  files[5]: 'brown'}
        # self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'dotted',
        #                              files[2]: 'solid', files[3]: 'dashed', files[4]: 'solid', files[5]: 'dotted'}
        #
        # self.process_dict = {files[0]: ['relative_returns'], files[1]: ['to_daily'],
        #                      files[2]: ['to_monthly'],
        #                      files[3]: ['to_weekly'], files[4]: ['to_quarterly'],
        #                      files[5]: ['to_yearly', 'clean']}
        # self.ymin = -23
        # self.ymax = 45
        # self.ylabel = 'percentage'


        # 'B202RC1Q027SBEA_PC1',
        # self.ecb_bool = False
        # self.fed_bool = True
        # self.folder_name = 'us_inflation_oil/'
        # self.plot_title = 'Correlations of the interest rate, crude oil, government wages with CPI for US'
        # files = ['CPIAUCSL_PC1', 'CPILFESL_PC1', 'DCOILBRENTEU', 'FEDFUNDS']
        # self.plot_legend_names = {files[0]: '% Change CPI of All Urban Consumers: All items in U.S. City Average',
        #                           files[1]: '% Change CPI for All Urban Consumers: All Items Less Food and Energy in '
        #                                     'U.S. City Average',
        #                           files[2]: 'Dollars per barrel crude oil Prices: Brent - Europe / 10',
        #                           files[3]: 'Federal Funds Effective Rate'}
        # self.plot_colors = {files[0]: 'blue', files[1]: 'darkblue', files[2]: 'red',
        #                     files[3]: 'green'}
        # self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'dashed', files[2]: 'solid',
        #                              files[3]: 'solid'}
        #
        # self.process_dict = {files[0]: ['time_window'], files[1]: ['time_window'],
        #                      files[2]: ['time_window', 'division_10'],
        #                      files[3]: ['time_window']}
        #
        # self.ymin = -3
        # self.ymax = 20
        # self.ylabel = 'percentage/value'

        # self.ecb_bool = False
        # self.fed_bool = True
        # self.folder_name = 'eu_inflation_oil/'
        # self.plot_title = 'Correlations of the interest rate, crude oil with CPI for EU'
        # files = ['CP0000EZ19M086NEST_PC1', 'DCOILBRENTEU', 'IRSTCI01EZM156N']
        # self.plot_legend_names = {files[0]: '% Change HICP: All items for Euro Area (19 Countries)',
        #                           files[1]: 'Crude Oil Prices: Brent - Europe / 10',
        #                           files[2]: 'Interest rates: Immediate Interbank Rates (< 24 Hours) Total for '
        #                                     'Euro Area (19 Countries)'}
        # self.plot_colors = {files[0]: 'blue', files[1]: 'red', files[2]: 'green'}
        # self.plot_linestyles_dict = {files[0]: 'solid', files[1]: 'solid', files[2]: 'solid'}
        #
        # self.process_dict = {files[0]: ['time_window'], files[1]: ['time_window', 'division_10'],
        #                      files[2]: ['time_window']}
        #
        # self.ymin = -3
        # self.ymax = 20
        # self.ylabel = 'percentage/value'


        # ,
        #                                   files[1]: '% Change CPI for All Urban Consumers: All Items Less Food and Energy in U.S. '
        #                                             'City Average'

        df_dict = {}
        if self.fed_bool:
            self.cb_folder = 'data_fed/'
        elif self.ecb_bool:
            self.cb_folder = 'data_ecb/'
        else:
            self.cb_folder = 'data_fed/'

    def test_parameters(self):


        if not isinstance(self.start_date, pd.Timestamp):
            raise Exception('start_date in config is not of type pd.Timestamp.')
        
        if not isinstance(self.end_date, pd.Timestamp):
            raise Exception('end_date in config is not of type pd.Timestamp.')
        
        if not isinstance(self.freq, str):
            raise Exception('freq in config is not of type str.')
        
        if not isinstance(self.returns_bool, bool):
            raise Exception('returns_bool in config is not of type bool.')

        if not isinstance(self.lag, int):
            raise Exception('lag in config is not of type int.')
        
        if not isinstance(self.clean_bool, bool):
            raise Exception('clean_bool in config is not of type bool.')

        if not isinstance(self.data_folder_path, str):
            raise Exception('data_folder_path in config is not of type str.')

        if not isinstance(self.output_path, str):
            raise Exception('output_path in config is not of type str.')
        
        if not isinstance(self.output_path, str):
            raise Exception('output_path in config is not of type str.')

        if not isinstance(self.ecb_fed_bool, bool):
            raise Exception('ecb_fed_bool in config is not of type bool.')

        if not isinstance(self.plot_type, str):
            raise Exception('plot_type in config is not of type str.')

        if not isinstance(self.window_size, int):
            raise Exception('window_size in config is not of type int.')
        
        if not isinstance(self.ecb_bool, bool):
            raise Exception('ecb_bool in config is not of type bool.')

        if not isinstance(self.fed_bool, bool):
            raise Exception('fed_bool in config is not of type bool.')

        if not isinstance(self.folder_name, str):
            raise Exception('folder_name in config is not of type str.')
        
        if not isinstance(self.plot_title, str):
            raise Exception('plot_title in config is not of type str.')
                
        if not isinstance(self.plot_legend_names, dict):
            raise Exception('plot_legend_names in config is not of type dict.')

        if not isinstance(self.plot_colors, dict):
            raise Exception('plot_colors in config is not of type dict.')
        
        if not isinstance(self.plot_linestyles_dict, dict):
            raise Exception('plot_linestyles_dict in config is not of type dict.')
        
        if not isinstance(self.process_dict, dict):
            raise Exception('process_dict in config is not of type dict.')
        
        if not isinstance(self.ymin, int):
            raise Exception('ymin in config is not of type float.')
        
        if not isinstance(self.ymax, int):
            raise Exception('ymax in config is not of type float.')
        
        if not isinstance(self.ylabel, str):
            raise Exception('ylabel in config is not of type str.')
        
        if not isinstance(self.regression_type, str):
            raise Exception('regression_type in config is not of type str.')

        if not isinstance(self.y_var, str):
            raise Exception('y_var in config is not of type str.')

        if not isinstance(self.x_vars_list, list):
            raise Exception('x_vars_list in config is not of type list[str].')

        if not isinstance(self.estimation_data_list, list):
            raise Exception('estimation_data_list in config is not of type list[str].')            
        
        if not isinstance(self.backtest_data_list, list):
            raise Exception('backtest_data_list in config is not of type list[str].')

        if not isinstance(self.strategy_list, list):
            raise Exception('strategy_list in config is not of type list[str].')   
        
        if not isinstance(self.objective_list, list):
            raise Exception('objective_list in config is not of type list[str].')   
        
        if not isinstance(self.transaction_cost_bool, bool):
            raise Exception('transaction_cost_bool in config is not of type bool.')   
             
        if not isinstance(self.transaction_cost_list, list):
            raise Exception('transaction_cost_list in config is not of type list.')   
             
        if not isinstance(self.transaction_cost, float):
            raise Exception('transaction_cost in config is not of type float.')   
             
        if not (len(self.transaction_cost_list) == len(self.objective_list) == len(self.strategy_list)):
           raise Exception('self.transaction_cost_list, self.objective_list and self.strategy_list must be of the same lenght.') 

        if (self.regression_type == 'granger') & (len(self.x_vars_list) + 1 > 2):
            raise Exception('Granger causality can only be computed among a pair of variables. '
                            'Make sure that y_var + x_vars_list is not larger than 2 variables.')

        correct_process_list = ['to_daily', 'to_weekly', 'to_monthly', 'to_quarterly', 'to_yearly', 'relative_returns',
                                'clean', 'compute_change', 'division_10', 'division_1m', 'division_1t', 'minus', 'lag_1',
                                'to_first_of_month', 'lag_3', 'lag_6', 'lag_12', 'time_window']

        process_list = [item for sublist in self.process_dict.values() for item in sublist]
        for process in process_list:
            if process not in correct_process_list:
                raise Exception('Process type is incorrectly specified. Choose from: '
                                'to_daily, to_weekly, to_monthly, to_quarterly, to_yearly, relative_returns, '
                                'clean, compute_change, division_10, division_1m, division_1t, minus, lag_1, '
                                'to_first_of_month, lag_3, lag_6, lag_12, time_window')

        
        correct_strategy_list = ['mean_strat']
        correct_objective_list = ['obj_sum']
        correct_transaction_cost_list = ['proportional_cost']

        self.check_settings_list(self.strategy_list, correct_strategy_list)
        self.check_settings_list(self.objective_list, correct_objective_list)
        self.check_settings_list(self.transaction_cost_list, correct_transaction_cost_list)

    @staticmethod
    def check_settings_list(settings_list: list[str], correct_settings_list: list[str]):
        for setting in settings_list:
            if setting not in correct_settings_list:
                raise Exception(f'Settings list {settings_list} is incorrectly specified. Choose from: {correct_settings_list}.')

        #         self.fed_files = ['fed_cpi', 'fed_deficit', 'fed_crude_oil', 'fed_population', 'fed_gdp',
        #                       'fed_usd_ger', 'fed_usd_yen', 'fed_usd_china', 'fed_M1SL', 'fed_M2SL', 'fed_M3SL', 'fed_FEDFUNDS',
        #                       'fed_bolivar_usd', 'fed_cpi_venezuela']
        #
        #         self.ecb_files = ['ecb_hicp', 'ecb_commodity_index', 'ecb_debt', 'ecb_gdp', 'ecb_m1', 'ecb_m2', 'ecb_m3',
        #                            'ecb_unemployment', 'ecb_interbank_lending_rate', 'ecb_crude_oil', 'ecb_household_loans',
        #                            'ecb_nfi_loans', 'ecb_private_consumption', 'ecb_credit_for_consumption_househols']