import base64

from base64_course.base64 import b64encode, b64decode


def test_b64encode():
    assert b64encode(b'Phoenix') == base64.b64encode(b'Phoenix')
    assert b64encode('凤'.encode()) == base64.b64encode('凤'.encode())

def test_b64decode():
    assert b64decode(b'UGhvZW5peA==') == base64.b64decode(b'UGhvZW5peA==')
