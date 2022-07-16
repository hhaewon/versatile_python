from flask.testing import FlaskClient
from flask import Flask
from werkzeug.test import TestResponse
from json import loads
from app import app, decode_value


def test_index():
    client = app.test_client()
    resp = client.get('/')
    assert b'<a href="/decode">to decode</a>' in resp.data
    assert resp.status_code == 200


def test_decode():
    client = app.test_client()
    data: dict = {
        'value': 'hello world',
        'language': 'en',
        'key': 12,
        'mode': 'encrypt',
    }
    resp: TestResponse = client.post('/decode',
                                     json=data,
                                     content_type='application/json')
    json_data = loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert json_data == decode_value(**data)
