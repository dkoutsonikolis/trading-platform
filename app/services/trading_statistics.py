import logging
from typing import Any, Protocol

from app.data_structures.exceptions import SegmentTreeCapacityLimitReachedException
from app.services.exceptions import TradingStatisticsServiceException, TradingStatisticsServiceSymbolDataLimitReachedException, TradingStatisticsServiceSymbolNotFoundException, TradingStatisticsServiceSymbolsLimitReachedException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StatisticalDataStructure(Protocol):
    def build(self, data: list[float]) -> None:
        """Builds the data structure with an initial dataset."""
    
    def append_data(self, data: list[float]) -> None:
        """Appends new data to the existing data structure."""
    
    def query(self, k: int) -> tuple[float, float, float, float, float]:
        """Queries statistical data (min, max, last, avg, variance) for the last 10^k data points."""

class TradingStatisticsService:
    MAX_SYMBOLS_NUMBER = 10

    def __init__(self, data_engine: StatisticalDataStructure) -> None:
        """
        Initialize the TradingStatisticsService with a data engine that adheres to the StatisticalDataStructure protocol.
        
        Args:
            data_engine: An implementation of the StatisticalDataStructure protocol (e.g., SegmentTree).
        """
        self.data_storage: dict[str, StatisticalDataStructure] = {}
        self.data_engine = data_engine

    def add_batch(self, symbol: str, values: list[float]) -> None:
        """
        Adds a batch of data for a specific symbol. If the symbol already exists, appends the new data.

        Args:
            symbol: The symbol representing the trading data (e.g., "AAPL").
            values: A list of data points (e.g., stock prices) to add to the engine.
        """
        try:
            if symbol not in self.data_storage:
                if len(self.data_storage) >= self.MAX_SYMBOLS_NUMBER:
                    logger.error(f"Symbol limit reached. Cannot add {symbol}.")
                    raise TradingStatisticsServiceSymbolsLimitReachedException()
                logger.info(f"Creating new data engine for symbol {symbol} and adding batch.")
                self.data_storage[symbol] = self.data_engine()
                self.data_storage[symbol].build(values)
            else:
                self.data_storage[symbol].append_data(values)
        
        except SegmentTreeCapacityLimitReachedException as e:
            logger.error(f"Error adding batch for symbol {symbol}: {str(e)}")
            raise TradingStatisticsServiceSymbolDataLimitReachedException() from e


    def get_stats(self, symbol: str, window_size_exponent: int) -> dict[str, float]:
        """
        Retrieves statistical data for a given symbol and a range defined by the window size exponent.
        
        Args:
            symbol: The symbol to retrieve stats for (e.g., "AAPL").
            window_size_exponent: The exponent that defines the range of the query as 10^k.
            
        Returns:
            A dictionary containing statistical data (min, max, last, avg, var).
        """
        try:
            result = self.data_storage[symbol].query(window_size_exponent)
        except KeyError:
            raise TradingStatisticsServiceSymbolNotFoundException(f"Symbol {symbol} not found.")
        return {
            "min": result[0],
            "max": result[1],
            "last": result[2],
            "avg": result[3],
            "var": result[4]
        }
