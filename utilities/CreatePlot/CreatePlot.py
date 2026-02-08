import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from utilities.Regressor.Regressor import Regressor
import pandas as pd

class CreatePlot:
    def __init__(self, pdf: PdfPages, ylabel: str):
        self.pdf = pdf
        self.ylabel = ylabel

    def line_plot_with_info(self, title: str, raw_df_dict: dict):
        list_col_names = []
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        fig, ax = plt.subplots(figsize=(18, 10))

        for name_df in raw_df_dict:
            x = raw_df_dict[name_df]['DATE']
            y = raw_df_dict[name_df].iloc[:, 1]

            plt.plot(x, y, linewidth=2.5)
            list_col_names.append(raw_df_dict[name_df].columns[1])
            data_concat = pd.concat([raw_df_dict[name_df].iloc[:, 1], raw_df_dict[name_df].iloc[:, 1]], axis=1)
            rho = data_concat.corr().iloc[1, 0]
            regressor = Regressor(data_concat)
            df_table = regressor.compute_ols(raw_df_dict[name_df].columns[1], raw_df_dict[name_df].columns[1])

            const = df_table['param_sig'].iloc[0]
            beta = df_table['param_sig'].iloc[1]
            textstr = '\n'.join((raw_df_dict[name_df].columns[1][4:] + ' vs ' + raw_df_dict[name_df].columns[1][4:],
                                 r'$\rho=%.2f$' % (rho,),
                                 r'const = ' + const,
                                 r'$\beta$ = ' + beta))
            ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox=props)
            plt.title(title)
            plt.xlabel('DATE')
            plt.ylabel('VALUE')
            plt.legend(list_col_names, loc='upper left')
            self.pdf.savefig()
            plt.close()

    def line_plot(self, df_dict: dict, title: str, colors_dict: dict, linestyle_dict: dict, legend_dict: dict, y_min: float, y_max: float):
        list_legend = []
        plt.figure(figsize=(18, 10))
        for name_df in df_dict:
            x = df_dict[name_df].iloc[:, 0]
            y = df_dict[name_df].iloc[:, 1]
            plt.plot(x, y, color=colors_dict[name_df], linestyle=linestyle_dict[name_df], linewidth=2.5)
            list_legend.append(legend_dict[name_df])
        plt.axhline(y=0, color='black', linestyle='-')
        plt.title(title, fontsize=22)
        plt.xlabel('time', fontsize=20)
        plt.ylabel(self.ylabel, fontsize=20)
        plt.ylim(y_min, y_max)
        plt.legend(list_legend,
                   fontsize=20, loc='upper left')
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        self.pdf.savefig()
        plt.close()

    def stem_plot(self, title: str, df_dict: dict):
        list_col_names = []
        plt.figure(figsize=(18, 10))
        for name_df in df_dict:
            x = df_dict[name_df]['DATE']
            y = df_dict[name_df].iloc[:, 1]
            plt.plot(x, y, linewidth=2.5)
            plt.fill_between(x, y, interpolate=True, color='blue')
            list_col_names.append(df_dict[name_df].columns[1])
        plt.axhline(y=0, color='black', linestyle='-')
        plt.title(title, fontsize=22)
        plt.xlabel('time', fontsize=20)
        plt.ylabel('value', fontsize=20)
        plt.legend(list_col_names,
                   fontsize=20)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        self.pdf.savefig()
        plt.close()
