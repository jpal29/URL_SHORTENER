import pytest
from shortener.encode import toBase64
import base64

from shortener.db import get_db

def test_index(client):
    response = client.get('/')
    assert b"The one stop shop for url shortening." in response.data


def test_url_shorten(app, client, auth):
    auth.login()
    assert client.get('/shorten').status_code == 200
    url = 'https://www.google.com'
    response = client.post('/', data={'url': url}, follow_redirects=True)
    assert response.status_code == 200

    # url is string and it needs to be encoded in bytes to be b64 encoded
    encoded_url = str.encode(url)
    b64_url = base64.urlsafe_b64encode(encoded_url)
    # b64_url is in bytes and it needs to be converted to string to be inserted in db table
    decoded_b64_url = b64_url.decode()

    with app.app_context():
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute('SELECT id FROM urls where url=%s', (decoded_b64_url,))
        db_response = db_cursor.fetchone()
        id = db_response[0]
        assert id is not None
        #toBase64 returns a str type and needs to be in byte format to compare to response.data
        assert str.encode(toBase64(id)) in response.data

