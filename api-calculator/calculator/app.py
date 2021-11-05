from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

tracer = Tracer()
logger = Logger()
metrics = Metrics()
app = ApiGatewayResolver()


@app.get("/calculator/operations")
def calculator_operations():
    return [
        {"operation": "sum", "path": "/calculator/sum", "method": "POST"},
        {"operation": "multiplication", "path": "/calculator/multiplication", "method": "POST"}
    ]


@app.post("/calculator/sum")
def calculator_sum():
    json_payload = app.current_event.json_body

    return {"result": json_payload["value_1"] + json_payload["value_2"]}


@app.post("/calculator/multiplication")
def calculator_multiplication():
    json_payload = app.current_event.json_body

    return {"result": json_payload["value_1"] * json_payload["value_2"]}


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
