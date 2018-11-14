import pytest
from flask import g, session
import json
from shortener.db import get_db

def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get('/auth/register').status_code == 200

    # test that successful registration redirects to the index page
    response = client.post(
         '/auth/register', data={'username': 'a', 'password': 'a'}
    )

    print('-------------------This is the response------------------------')
    for section in response.headers:
        print(section)
    #print(len(response.headers))
    print('----------------------------------------------------------------')

    assert 'http://localhost/' == response.headers['Location']

    #test that the user was inserted into the database
    with app.app_context():
        db = get_db()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute(
            "select * from users where username='a'"
        )

        assert db_cursor.fetchone() is not None

# @pytest.mark.parametrize(('username', 'password', 'message'), (
#         ('', '', b'Username is required.'),
#         ('a', '', b'Password is required.'),
#         ('test', 'test', b'already registered'),
# ))
# def test_register_validate_input(client, username, password, message):
#     response = client.post(
#         '/auth/register',
#         data={'username': username, 'password': password}
#     )
#     print('-------------------This is the response------------------------')
#     print(response)
#     print('----------------------------------------------------------------')
#     print('-------------------This is the response text--------------------')
#     print(response.body)
#     print('-----------------------------------------------------------------')
#     assert response.message