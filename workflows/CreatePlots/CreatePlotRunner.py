import os
from matplotlib.backends.backend_pdf import PdfPages
from workflows.AbstractTestRunner import AbstractTestRunner
from config.Config import Config
from utilities.CreatePlot import CreatePlot


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
        self.y_min = config.y_min
        self.y_max = config.y_max
        self.ylabel = config.ylabel

    def run(self, df_dict: dict):
        pdf = PdfPages(self.output_path + self.title + '.pdf')
        create_plot = CreatePlot(pdf, self.ylabel)
        if self.plot_type == 'line':
            create_plot.line_plot(df_dict, self.title, self.colors_dict, self.linestyle_dict, self.legend_dict , self.y_min, self.y_max)
        elif self.plot_type == 'line_with_info':
            create_plot.line_plot_with_info(self.title, self.colors_dict)
        elif self.plot_type == 'stem':
            create_plot.stem_plot(self.title, self.colors_dict)
        else:
            raise Exception('plot_type incorrectly specified as: ' + self.plot_type +
                            'choose from [line, line_with_info, stem] instead!')
        pdf.close()




