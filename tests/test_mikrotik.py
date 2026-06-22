from mikrotik.client import connect


def test_connect_function_exists():
    assert callable(connect)
