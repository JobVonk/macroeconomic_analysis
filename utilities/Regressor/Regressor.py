import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests
import numpy as np
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller, kpss


class Regressor:
    """" The regressor class can perform several regressions on the data such as OLS. """

    def __init__(self, data: dict, y_var: str, x_vars_list: list[str]):
        self.data = data
        self.y_var = y_var
        self.x_vars_list = x_vars_list
        self.regressor_dict = {'ols': self.compute_ols, 'granger': self.compute_granger_causality,
                               'var': self.compute_var}

    def run(self, regression_type: str):

        concat_dfs = self.preprocess(self.y_var, self.x_vars_list)
        y = concat_dfs[self.y_var]
        y.index = concat_dfs.index
        y = y.to_numpy()

        x = concat_dfs[self.x_vars_list]
        x.index = concat_dfs.index
        x = x.to_numpy()
        self.check_stationarity(concat_dfs)
        self.regressor_dict[regression_type](y, x)

    def preprocess(self, y_var: str, x_vars_list: list[str]) -> pd.DataFrame:
        concat_list = [y_var] + x_vars_list
        concat_dfs = self.concat_dfs(concat_list)
        return concat_dfs

    def compute_ols(self, y: np.array, x: np.array):
        model = sm.OLS(y, x, cov_type='HC1').fit()
        df_model = self.model_output_to_df(model)
        df_table = self.create_table_ols(df_model)
        print(df_table.to_latex(index=False))
        print(model.summary())
        return df_table

    def compute_granger_causality(self, y: np.array, x: np.array, max_lag=3) -> pd.DataFrame:
        concat_array = np.concatenate([y.reshape(len(y), 1), x], axis=1)
        granger_result = grangercausalitytests(concat_array, maxlag=max_lag, verbose=True)
        df = self.granger_causality_to_df(granger_result)
        print(df.round(3).to_latex(index=False))
        return df

    def concat_dfs(self, concat_df_list: list[str]) -> pd.DataFrame:
        concat_dfs = pd.DataFrame()
        for arg in concat_df_list:
            df = self.data[arg]
            df.index = self.data[arg]['DATE']
            concat_dfs = pd.concat([concat_dfs, df], axis=1)
        concat_dfs.dropna(inplace=True)
        concat_dfs = concat_dfs[concat_df_list]
        return concat_dfs

    @staticmethod
    def granger_causality_to_df(granger_results) -> pd.DataFrame:
        results = []
        for lag, res in granger_results.items():
            p_values = {key: val[1] for key, val in res[0].items()}
            p_values['lag'] = lag
            results.append(p_values)
        df = pd.DataFrame(results)
        return df

    @staticmethod
    def check_stationarity(concat_dfs: pd.DataFrame):
        output_df = pd.DataFrame()
        for df_col in concat_dfs.columns:
            series = concat_dfs[df_col]
            adf_result = adfuller(series)
            kpss_result = kpss(series)
            test_df = pd.DataFrame([df_col, adf_result[0], adf_result[4]['5%'], adf_result[1],
                                      kpss_result[0], kpss_result[3]['5%'], kpss_result[1], len(series)],
                                     index=['var', 'adf crit.', 'adf cut-off 5%', 'adf p-value',
                                            'kpss crit.', 'kpss cut-off 5%', 'kpss p-value', 'nr. obs']).T
            output_df = pd.concat([output_df, test_df])
        print(output_df.to_latex(index=False))

    def compute_var(self, y: np.array, x: np.array):
        concat_array = np.concatenate([y.reshape(len(y), 1), x], axis=1)

        model = VAR(concat_array)
        max_lags = 5
        var_results = model.fit(maxlags=5, ic='aic')
        self.create_var_table(var_results)
        b=3

        # # Step 3: Forecasting
        # print("\nStep 3: Forecasting")
        # lag_order = results.k_ar
        # forecast = results.forecast(data.values[-lag_order:], steps=10)
        #
        # # Step 4: Visualizing forecast
        # print("\nStep 4: Visualizing forecast")
        # forecast_index = pd.date_range(start='2024-04-11', periods=10)
        # forecast_data = pd.DataFrame(forecast, index=forecast_index, columns=data.columns)

    def create_table_ols(self, df_model: pd.DataFrame) -> pd.DataFrame:
        round_n = 3
        param_list = df_model['param'].to_list()
        p_value_list = df_model['p-value'].to_list()
        sig_level_list = self.add_sig_stars(param_list, p_value_list, round_n)
        #df_table = pd.DataFrame(sig_level_list, index=df_model.index, columns=['param_sig'])
        df_model = df_model.round(round_n)
        df_model['param'] = sig_level_list
        return df_model

    def create_var_table(self, var_results):
        round_n = 3
        params_list = list(var_results.params.flatten(order='F'))
        pvalues_list = list(var_results.pvalues.flatten(order='F'))
        tvalues_list = list(var_results.tvalues.flatten(order='F'))
        std_err_list = list(var_results.stderr.flatten(order='F'))

        sig_level_list = self.add_sig_stars(params_list, pvalues_list, round_n)

        table_df = pd.DataFrame([std_err_list, tvalues_list, pvalues_list]).T
        table_df = table_df.round(round_n)
        table_df.insert(0, 'params', sig_level_list)
        vars_list = [self.y_var] + self.x_vars_list
        index_list = []
        for var in vars_list:
             index_list = index_list + ['const'] + ['L' + str(lag) + '_' + var for lag in np.arange(var_results.params.shape[0]-1)]
        table_df.index = var_results.exog_names * len(vars_list)
        table_df.columns = ['params', 'std. err.', 't-stat', 'p-value']
        print(table_df.to_latex())
        print(var_results.summary())
        # coefs_df = pd.DataFrame(np.array(sig_level_list).reshape(3, 2))

        b=3

    @staticmethod
    def model_output_to_df(model) -> pd.DataFrame:
        df = pd.DataFrame(np.concatenate([model.params.reshape(model.params.shape[0], 1),
                                          model.bse.reshape(model.bse.shape[0], 1),
                                          model.tvalues.reshape(model.tvalues.shape[0], 1),
                                          model.pvalues.reshape(model.pvalues.shape[0], 1)], axis=1))
        df.columns = ['param', 'std. err.', 't stat.', 'p-value']
        return df

    @staticmethod
    def add_sig_stars(param_list: list[float], p_value_list: list[float], round_n: int) -> list[str]:
        sig_level_list = []
        for idx in range(0, len(p_value_list)):
            p_value = p_value_list[idx]
            param = param_list[idx]
            if p_value < 0.01:
                sig_level = str(round(param, round_n)) + '***'
            elif p_value < 0.05:
                sig_level = str(round(param, round_n)) + '**'
            elif p_value < 0.1:
                sig_level = str(round(param, round_n)) + '*'
            else:
                sig_level = str(round(param, round_n))
            sig_level_list.append(sig_level)
        return sig_level_list

    #
    # @staticmethod
    # def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #     df = df[~df.isin([np.nan, np.inf, -np.inf])]
    #     return df

