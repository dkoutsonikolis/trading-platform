import unittest
from unittest.mock import MagicMock
from app.data_structures.exceptions import SegmentTreeCapacityLimitReachedException
from app.data_structures.segment_tree import SegmentTree
from app.services.exceptions import TradingStatisticsServiceException, TradingStatisticsServiceSymbolDataLimitReachedException, TradingStatisticsServiceSymbolNotFoundException, TradingStatisticsServiceSymbolsLimitReachedException
from app.services.trading_statistics import TradingStatisticsService

class TestTradingStatisticsService(unittest.TestCase):
    
    def setUp(self):
        self.mock_data_engine = MagicMock()
        self.mock_data_engine.return_value.query.return_value = (1, 10, 5, 2.5, 1)
        
        self.service = TradingStatisticsService(self.mock_data_engine)
    
    def test_add_batch_new_symbol(self):
        symbol = "AAPL"
        values = [100, 200, 300, 400]
        
        self.service.add_batch(symbol, values)
        
        self.mock_data_engine.return_value.build.assert_called_once_with(values)
        self.assertIn(symbol, self.service.data_storage)
    
    def test_add_batch_existing_symbol(self):
        symbol = "AAPL"
        values = [100, 200, 300, 400]
        
        self.service.add_batch(symbol, values)
        
        new_values = [500, 600, 700]
        
        self.service.add_batch(symbol, new_values)

        self.mock_data_engine.return_value.build.assert_called_with(values)
        self.mock_data_engine.return_value.append_data.assert_called_once_with(new_values)

        self.assertIn(symbol, self.service.data_storage)
    
    def test_get_stats_success(self):
        symbol = "AAPL"
        window_size_exponent = 2  # 10^2 = 100
        
        self.service.add_batch(symbol, [100, 200, 300, 400])
        
        stats = self.service.get_stats(symbol, window_size_exponent)
        
        self.assertEqual(stats["min"], 1)
        self.assertEqual(stats["max"], 10)
        self.assertEqual(stats["last"], 5)
        self.assertEqual(stats["avg"], 2.5)
        self.assertEqual(stats["var"], 1)
    
    def test_add_batch_symbols_limit_reached(self):
        self.service.MAX_SYMBOLS_NUMBER = 2
        
        self.service.add_batch("AAPL", [100, 200, 300, 400])
        self.service.add_batch("GOOG", [500, 600, 700, 800])
        
        with self.assertRaises(TradingStatisticsServiceSymbolsLimitReachedException):
            self.service.add_batch("AMZN", [100, 200, 300, 400])
    
    def test_get_stats_symbol_not_found(self):
        with self.assertRaises(TradingStatisticsServiceSymbolNotFoundException):
            self.service.get_stats("AAPL", 2)  # Symbol does not exist
    
    def test_add_batch_symbol_data_limit_reached(self):
        symbol = "AAPL"
        values = [100, 200, 300, 400]
        
        self.mock_data_engine.return_value.build.side_effect = SegmentTreeCapacityLimitReachedException()
        
        with self.assertRaises(TradingStatisticsServiceSymbolDataLimitReachedException) as context:
            self.service.add_batch(symbol, values)



