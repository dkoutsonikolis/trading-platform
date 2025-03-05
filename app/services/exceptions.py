class TradingStatisticsServiceException(Exception):
    pass

class TradingStatisticsServiceSymbolsLimitReachedException(TradingStatisticsServiceException):
    pass

class TradingStatisticsServiceSymbolDataLimitReachedException(TradingStatisticsServiceException):
    pass

class TradingStatisticsServiceSymbolNotFoundException(TradingStatisticsServiceException):
    pass
