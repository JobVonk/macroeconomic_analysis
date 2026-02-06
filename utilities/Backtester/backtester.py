from utilities.DataContainer.DataContainer import DataContainer


class Backtester:
    def __init__(self, data_container: DataContainer, window_size: int):
        self.data_container = data_container
        self.window_size = window_size

    def run(self):
        self.data_container
        
