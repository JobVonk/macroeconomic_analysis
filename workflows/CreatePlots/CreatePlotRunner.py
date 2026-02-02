import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from workflows.AbstractTestRunner import AbstractTestRunner
import pandas as pd
from utilities.Regressor.Regressor import Regressor
from config.Config import Config


class CreatePlotRunner(AbstractTestRunner):
    """" This class creates formatted plots using one or multiple data sources"""
    def __init__(self, config: Config):
        self.output_path = config.output_path + 'plots/'
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        self.plot_type = config.plot_type
        self.title = config.plot_title
        self.colors_dict = config.plot_colors
        self.legend_dict = config.plot_legend_names
        self.linestyle_dict = config.plot_linestyles_dict
        self.ymin = config.ymin
        self.ymax = config.ymax
        self.ylabel = config.ylabel

    def run(self, df_dict: dict):
        pdf = PdfPages(self.output_path + self.title + '.pdf')
        if self.plot_type == 'line':
            self.line_plot(pdf, df_dict)
        elif self.plot_type == 'line_with_info':
            self.line_plot_with_info(pdf, self.title, self.colors_dict)
        elif self.plot_type == 'stem':
            self.stem_plot(pdf, self.title, self.colors_dict)
        else:
            raise Exception('plot_type incorrectly specified as: ' + self.plot_type +
                            'choose from [line, line_with_info, stem] instead!')
        pdf.close()

    @staticmethod
    def line_plot_with_info(pdf: PdfPages, title: str, raw_df_dict: dict):
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
            pdf.savefig()
            plt.close()

    def line_plot(self, pdf: PdfPages, df_dict: dict):
        list_legend = []
        plt.figure(figsize=(18, 10))
        for name_df in df_dict:
            x = df_dict[name_df].iloc[:, 0]
            y = df_dict[name_df].iloc[:, 1]
            plt.plot(x, y, color=self.colors_dict[name_df], linestyle=self.linestyle_dict[name_df], linewidth=2.5)
            list_legend.append(self.legend_dict[name_df])
        plt.axhline(y=0, color='black', linestyle='-')
        plt.title(self.title, fontsize=22)
        plt.xlabel('time', fontsize=20)
        plt.ylabel(self.ylabel, fontsize=20)
        plt.ylim(self.ymin, self.ymax)
        plt.legend(list_legend,
                   fontsize=20, loc='upper left')
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        pdf.savefig()
        plt.close()

    @staticmethod
    def stem_plot(pdf: PdfPages, title: str, df_dict: dict):
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
        pdf.savefig()
        plt.close()



