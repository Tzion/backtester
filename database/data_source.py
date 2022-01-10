from abc import ABC, abstractmethod, abstractproperty

PREFIX = 'database/data/'

class DataSource(ABC):

    @abstractmethod
    def get_feed_filename(self, symbol: str) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def get_feed_path(self, symbol: str) -> str:
        return PREFIX + '/' + self.name.lower() +'/' + self.get_feed_filename(symbol)
            

class IBDataSource(DataSource):

    def get_feed_filename(self, symbol: str):
        return symbol + '-STK-SMART-USD.csv'

    @property
    def name(self) -> str:
        return 'INTERACTIVE_BROKERS'