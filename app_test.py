import pytest
from flask.testing import FlaskClient
from flask import Flask
from werkzeug.test import TestResponse
from json import loads
from app import decode_value, create_app


@pytest.fixture
def api():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_index(api: TestResponse):
    client = api
    resp = client.get('/')
    assert b'<a href="/decode">to decode</a>' in resp.data
    assert resp.status_code == 200


def test_decode_en(api: TestResponse):
    client = api
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


def test_decode_ko(api: TestResponse):
    client = api
    data: dict = {
        'value': '안녕하세요',
        'language': 'ko',
        'key': 10000,
        'mode': 'encrypt',
    }
    resp: TestResponse = client.post('/decode',
                                     json=data,
                                     content_type='application/json')
    json_data = loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert json_data == decode_value(**data)
