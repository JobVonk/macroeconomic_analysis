import abc
from config.Config import Config


class AbstractTestRunner(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, df_dict: dict):
        ...

