from app import trading_stats_bp
from flask import Flask, request, jsonify
from app.services.trading_statistics import TradingStatisticsService
from app.services.exceptions import TradingStatisticsServiceException, TradingStatisticsServiceSymbolNotFoundException, TradingStatisticsServiceSymbolsLimitReachedException
from app.data_structures.segment_tree import SegmentTree 


service = TradingStatisticsService(data_engine=SegmentTree)

@trading_stats_bp.route('/add_batch/', methods=['POST'])
def add_batch():
    """
    Endpoint for adding a batch of trading data points for a specific symbol.
    """
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        values = data.get('values')

        if not symbol or not isinstance(values, list) or len(values) > 10000:
            return jsonify({'error': 'Invalid input, ensure symbol is provided and values is a list of up to 10000 floats'}), 400

        service.add_batch(symbol, values)
        return jsonify({'message': 'Batch data added successfully'}), 200

    except TradingStatisticsServiceException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@trading_stats_bp.route('/stats/', methods=['GET'])
def get_stats():
    """
    Endpoint for retrieving statistical data for a specific symbol and window size exponent (k).
    """
    try:
        symbol = request.args.get('symbol')
        k = request.args.get('k', type=int)

        if not symbol or k is None or not (1 <= k <= 8):
            return jsonify({'error': 'Invalid input, ensure symbol is provided and k is an integer between 1 and 8'}), 400

        stats = service.get_stats(symbol, k)

        return jsonify(stats), 200
    
    except TradingStatisticsServiceSymbolNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except TradingStatisticsServiceException as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

