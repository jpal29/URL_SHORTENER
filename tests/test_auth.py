import pytest
from flask import g, session
import json
from shortener.db import get_db

def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get('/auth/register').status_code == 200

    # test that successful registration redirects to the index page
    response = client.post(
         '/auth/register', data={'username': 'testing', 'password': 'testing'}
    )
    assert 'Path=/' in response.headers[2][1]

    #test that the user was inserted into the database
    with app.app_context():
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute(
            "select * from users where username='a'"
        )

        assert db_cursor.fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('testing', '', b'Password is required.'),
        ('testing', 'testing', b'Username is taken, please use another.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )

    assert message in response.data


