import pytest

def test_index(client):
    response = client.get('/')
    assert b"The one stop shop for url shortening." in response.data


def test_url_shorten(client, auth, app):
    auth.login()
    assert client.get('/shorten').status_code == 200
