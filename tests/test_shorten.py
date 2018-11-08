import pytest

def test_index(client):
    response = client.get('/')
    assert b"Index Page" in response.data