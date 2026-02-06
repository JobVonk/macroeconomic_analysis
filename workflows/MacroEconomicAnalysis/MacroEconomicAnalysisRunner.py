from workflows.AbstractTestRunner import AbstractTestRunner
from utilities.Regressor.Regressor import Regressor
from config.Config import Config


class MacroEconomicAnalysisRunner(AbstractTestRunner):
    def __init__(self, config: Config):
        self.config = config
        self.regression_type = config.regression_type
        self.y_var = config.y_var
        self.x_vars_list = config.x_vars_list

    def run(self, df_dict: dict):
        regressor = Regressor(df_dict, self.y_var, self.x_vars_list)
        regressor.run(self.regression_type)
        
        #
        # granger_df = regressor.granger_causality_to_df(self.y_var, self.x_vars_list)
        # oil = df_dict['DCOILBRENTEU']
        # oil['DCOILBRENTEU'] = oil['DCOILBRENTEU']/10
        # df_dict['DCOILBRENTEU'] = oil
        # new_names_dict = dict(CPIAUCSL_PC1='CPI for All Urban Consumers: All Items in U.S. City Average ',
        #      CPILFESL_CH1='CPI for All Urban Consumers: All Items Less Food and Energy in U.S. City Average',
        #      DCOILBRENTEU='Crude Oil Prices: Brent - Europe', FEDFUNDS='Federal Funds Effective Rate')
        #
        # title = 'CPI vs Crude Oil vs Federal Funds Effective Rate'
        # edited_df_dict = data_container.change_column_names(edited_df_dict, new_names_dict)
        # edited_df_dict = data_container.change_dict_keys(edited_df_dict, new_names_dict)
        # colors = {'CPI for All Urban Consumers: All Items in U.S. City Average ': ['navy', 'solid'],
        #      'CPI for All Urban Consumers: All Items Less Food and Energy in U.S. City Average': ['blue', 'dashed'],
        #      'Crude Oil Prices: Brent - Europe': ['green', 'solid'], 'Federal Funds Effective Rate': ['red', 'solid']}
        # plot_runner = CreatePlotRunner(self.config, edited_df_dict)
        # plot_runner.run('line', title, colors, edited_df_dict)
        #
        # self.config.folder_name = 'fed_fund_cpi_m2/'
        # data_container = DataContainer(self.config)
        # edited_df_dict = data_container.edited_df_dict
        # # oil = edited_df_dict['DCOILBRENTEU']
        # # oil['DCOILBRENTEU'] = oil['DCOILBRENTEU']/10
        # # edited_df_dict['DCOILBRENTEU'] = oil
        # new_names_dict = dict(CPIAUCSL_PC1='CPI for All Urban Consumers: All Items in U.S. City Average ',
        #         CPILFESL_CH1='CPI for All Urban Consumers: All Items Less Food and Energy in U.S. City Average',
        #         FEDFUNDS='Federal Funds Effective Rate', M2REAL_CH1='Real M2 Money Stock', WM2NS_CH1='M2')
        #
        # title = 'Monetary aggregates vs the interest rate'
        # edited_df_dict = data_container.change_column_names(edited_df_dict, new_names_dict)
        # edited_df_dict = data_container.change_dict_keys(edited_df_dict, new_names_dict)
        # colors = {'CPI for All Urban Consumers: All Items in U.S. City Average ': ['navy', 'solid'],
        #      'CPI for All Urban Consumers: All Items Less Food and Energy in U.S. City Average': ['blue', 'dashed'],
        #     'Federal Funds Effective Rate': ['red', 'solid'],
        #           'Real M2 Money Stock': ['green', 'dashed'], 'M2': ['darkgreen', 'solid']}
        # plot_runner = CreatePlotRunner(self.config, edited_df_dict)
        # plot_runner.run('line', title, colors, edited_df_dict)
        #
        # new_names_dict = dict(CPIAUCSL_PC1='CPI for All Urban Consumers: All Items in U.S. City Average ',
        #                       CPILFESL_CH1='CPI for All Urban Consumers: All Items Less Food and Energy in U.S. City Average',
        #                       DCOILBRENTEU='OIL', )

        #df_regress = self.process_data(inputs_dict_returns)





        # y_var = 'ecb_nfi_loans'
        # 'ecb_household_loans'

        # 'ecb_nfi_loans'
        # regressor = Regressor(df_regress)
        # regressor.compute_ols(y_var, 'ecb_interbank_lending_rate')
        # # regressor.compute_granger_causality(y_var, 'ecb_gdp')
        #
        # create_plot_runner = CreatePlotRunner(self.output_path)
        # # create_plot_runner.run(hicp_ret, 'hicp returns')
        # # create_plot_runner.run(hicp_price, 'hicp price')
        #
        # ecb_household_loans = df_regress['ecb_household_loans']
        # ecb_household_loans = pd.DataFrame(ecb_household_loans, columns=['DATE', 'ecb_household_loans'])
        # ecb_household_loans['DATE'] = df_regress.iloc[:,0]
        #
        # ecb_unemployment = df_regress['ecb_unemployment']
        # ecb_unemployment = pd.DataFrame(ecb_unemployment, columns=['DATE', 'ecb_unemployment'])
        # ecb_unemployment['DATE'] = df_regress.iloc[:,0]
        #
        # ecb_interbank_lending_rate = df_regress['ecb_interbank_lending_rate']
        # ecb_interbank_lending_rate = pd.DataFrame(ecb_interbank_lending_rate, columns=['DATE', 'ecb_interbank_lending_rate'])
        # ecb_interbank_lending_rate['DATE'] = df_regress.iloc[:, 0]
        #
        # ecb_nfi_loans = df_regress['ecb_nfi_loans']
        # ecb_nfi_loans = pd.DataFrame(ecb_nfi_loans, columns=['DATE', 'ecb_nfi_loans'])
        # ecb_nfi_loans['DATE'] = df_regress.iloc[:, 0]
        #
        # create_plot_runner.run('line_with_info','correlation unemployment and the interest rate',
        #                        ecb_unemployment, ecb_interbank_lending_rate)



