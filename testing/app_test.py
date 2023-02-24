import pytest
import redis
import requests
from unittest.mock import patch
from app import app, _add_to_cache_and_log, _fib
 
from fastapi.testclient import TestClient
# client = TestClient(app)

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@patch.object(redis.Redis, 'get', return_value=None)
@patch.object(redis.Redis, 'exists', return_value=False)
def test_fibonacci_cache_miss(mock_exists, mock_get, client):
    response = client.get('/fib/5')

    assert response.status_code == 200
    assert int(response.content) == 5
    assert mock_exists.called_with(5)
    assert mock_get.called_with(5, None)
    assert redis.Redis().get(5) == b'5'

@patch.object(redis.Redis, 'get', return_value=b'5')
@patch.object(redis.Redis, 'exists', return_value=True)
def test_fibonacci_cache_hit(mock_exists, mock_get, client):
    response = client.get('/fib/5')

    assert response.status_code == 200
    assert int(response.content) == 5
    assert mock_exists.called_with(5)
    assert mock_get.called_with(5, None)
    assert redis.Redis().get(5) == b'5'

def test_fibonacci_negative_argument(client):
    response = client.get('/fib/-1')

    assert response.status_code == 422

def test_fibonacci_logging_cache_miss(client):
    with patch('app.logger.info') as mock_logger:
        client.get('/fib/6')

        mock_logger.assert_any_call('Cache for 6 not found.')

def test_fibonacci_logging_cache_hit(client):
    with patch('app.logger.info') as mock_logger:
        client.get('/fib/5')

        mock_logger.assert_any_call('Getting result for n = 5 from cache.')

def test_add_to_cache_and_log():
    with patch('app.cache.set') as mock_set:
        with patch('app.logger.info') as mock_logger:
            _add_to_cache_and_log(5, 5)

            mock_set.assert_called_with(5, 5)
            mock_logger.assert_any_call('Added to cache: 5: 5.')

def test_fibonacci():
    assert _fib(0) == 0
    assert _fib(1) == 1
    assert _fib(2) == 1
    assert _fib(3) == 2
    assert _fib(4) == 3
    assert _fib(5) == 5

 
# import pytest
# import json

# from fastapi.testclient import TestClient
# from unittest.mock import patch, MagicMock

# from app import app, cache


# @pytest.fixture
# def client():
#     with TestClient(app) as client:
#         yield client


# def test_get_fib_cache_hit(client):
#     # Add a value to cache
#     cache.set(1, 1)

#     # Make a request
#     response = client.get("/fib/1")

#     # Assert response
#     assert response.status_code == 200
#     assert int(response.content) == 1

#     # Assert logging
#     assert "Getting result for n = 1 from cache." in caplog.text


# def test_get_fib_cache_miss(client):
#     # Remove value from cache
#     cache.delete(1)

#     # Mock _fib function
#     with patch("app._fib", return_value=1) as mock_fib:
#         # Make a request
#         response = client.get("/fib/1")

#         # Assert response
#         assert response.status_code == 200
#         assert int(response.content) == 1

#         # Assert logging
#         assert "Cache for 1 not found." in caplog.text
#         assert "Added to cache: 1: 1." in caplog.text

#     # Assert _fib function was called
#     mock_fib.assert_called_once_with(1)


# def test_get_fib_invalid_input(client):
#     # Make a request with invalid input
#     response = client.get("/fib/-1")

#     # Assert response
#     assert response.status_code == 422
#     assert json.loads(response.content) == {"detail": "Invalid n value: -1"}

#     # Assert logging
#     assert "Invalid argument: -1." in caplog.text


# def test_get_fib_exception(client):
#     # Mock _fib function to raise an exception
#     with patch("app._fib", side_effect=Exception("Something went wrong.")) as mock_fib:
#         # Make a request
#         response = client.get("/fib/1")

#         # Assert response
#         assert response.status_code == 500
#         assert json.loads(response.content) == {"detail": "Internal server error"}

#         # Assert logging
#         assert "Something went wrong." in caplog.text

#     # Assert _fib function was called
#     mock_fib.assert_called_once_with(1)
