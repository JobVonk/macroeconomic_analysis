import abc
import pandas as pd
from workflows.AbstractTestRunner import AbstractTestRunner


class RealEstateAnalysisRunner(AbstractTestRunner):
    def __init__(self):
        self.files = ['\Gemiddelde_verkoopprijs_2023', '\Verkochte bestaande koopwoningen',
                 '\Prijzen bestaande koopwoningen']
        self.folder = r'C:\Users\jjvon\Documents\data\house_prices'
        self.data_houses_sold = pd.read_csv(self.folder + self.files[0] + '.csv')
        self.data_prices_houses = pd.read_csv(self.folder + self.files[1] + '.csv')
        self.data_prices_existing_houses = pd.read_csv(self.folder + self.files[2] + '.csv')

    def run(self):
        data = self.data_houses_sold

