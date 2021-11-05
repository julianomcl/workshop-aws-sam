import json

from calculator import app


def test_lambda_handler(sum_apigw_event, lambda_context):
    ret = app.lambda_handler(sum_apigw_event, lambda_context)
    expected = json.dumps({"result": 30}, separators=(",", ":"))

    assert ret["statusCode"] == 200
    assert ret["body"] == expected
