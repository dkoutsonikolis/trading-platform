import pytest
from flask import Flask
from app.services.exceptions import TradingStatisticsServiceSymbolNotFoundException
from app.data_structures.segment_tree import SegmentTree


ADD_BATCH_ENDPOINT = "/api/trading-statistics/add_batch/"
STATS_ENDPOINT = "/api/trading-statistics/stats/"


def test_add_batch(client):
    data = {
        "symbol": "AAPL",
        "values": [150.5, 151.0, 151.2, 149.5, 148.8]
    }

    # Send POST request
    response = client.post(ADD_BATCH_ENDPOINT, json=data)

    assert response.status_code == 200
    assert response.json == {"message": "Batch data added successfully"}


def test_add_batch_invalid_data(client):
    data = {
        "symbol": "AAPL",
        "values": "invalid_data"  # Invalid data type
    }

    # Send POST request
    response = client.post(ADD_BATCH_ENDPOINT, json=data)

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input, ensure symbol is provided and values is a list of up to 10000 floats'}

    # Test with an empty symbol
    data = {
        "symbol": "",
        "values": [150.5, 151.0]
    }
    response = client.post(ADD_BATCH_ENDPOINT, json=data)

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input, ensure symbol is provided and values is a list of up to 10000 floats'}

    # Test with more than 10,000 values
    data = {
        "symbol": "AAPL",
        "values": [1.0] * 10001
    }
    response = client.post(ADD_BATCH_ENDPOINT, json=data)

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input, ensure symbol is provided and values is a list of up to 10000 floats'}


def test_get_stats(client):
    data = {
        "symbol": "AAPL",
        "values": [150.5, 151.0, 151.2, 149.5, 148.8]
    }
    client.post(ADD_BATCH_ENDPOINT, json=data)

    response = client.get(f'{STATS_ENDPOINT}?symbol=AAPL&k=1')

    assert response.status_code == 200
    assert "min" in response.json
    assert "max" in response.json
    assert "last" in response.json
    assert "avg" in response.json
    assert "var" in response.json


def test_get_stats_symbol_not_found(client):
    response = client.get(f'{STATS_ENDPOINT}?symbol=NON_EXISTENT_SYMBOL&k=1')

    assert response.status_code == 404
    assert response.json == {'error': "Symbol NON_EXISTENT_SYMBOL not found."}


def test_get_stats_invalid_k(client):
    data = {
        "symbol": "AAPL",
        "values": [150.5, 151.0, 151.2, 149.5, 148.8]
    }
    client.post('/add_batch/', json=data)

    # Invalid k (out of range)
    response = client.get(f'{STATS_ENDPOINT}?symbol=AAPL&k=9')

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input, ensure symbol is provided and k is an integer between 1 and 8'}

    # Missing symbol
    response = client.get(f'{STATS_ENDPOINT}?k=3')

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input, ensure symbol is provided and k is an integer between 1 and 8'}

    # Missing k
    response = client.get(f'{STATS_ENDPOINT}?symbol=AAPL')

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input, ensure symbol is provided and k is an integer between 1 and 8'}
