import pandas as pd
from workflows.AbstractTestRunner import AbstractTestRunner


class DataAnalysisRunner(AbstractTestRunner):
    def __init__(self, data):
        self.data = data

    def run(self):
        b=3


