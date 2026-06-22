from billing.lipana import initiate_stk_push


def test_payment_api_function_exists():
    assert callable(initiate_stk_push)
