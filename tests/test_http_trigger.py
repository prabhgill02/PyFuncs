import sys
import os
import pytest
import azure.functions as func

# 👇 Add root directory to sys.path so Python can import function_app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from function_app import http_trigger  # ✅ Use the correct filename here

def build_request(method='GET', params=None, body=None):
    return func.HttpRequest(
        method=method,
        url='/api/http_trigger',
        headers={},
        params=params or {},
        body=body.encode('utf-8') if body else None
    )

def test_query_param_name():
    req = build_request(params={'name': 'Alice'})
    resp = http_trigger(req)
    assert resp.status_code == 200
    assert b"Alice" in resp.get_body()

def test_body_param_name():
    req = build_request(method='POST', body='{"name": "Bob"}')
    resp = http_trigger(req)
    assert resp.status_code == 200
    assert b"Bob" in resp.get_body()

def test_no_name():
    req = build_request(method='POST', body='{}')  
    resp = http_trigger(req)
    assert resp.status_code == 200
    assert b"Pass a name" in resp.get_body()
