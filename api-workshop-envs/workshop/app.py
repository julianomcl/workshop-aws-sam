import os

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

tracer = Tracer()
logger = Logger()
metrics = Metrics()
app = ApiGatewayResolver()


LINK_DRIVE = os.environ.get("LINK_DRIVE", "")


@app.get("/drive")
def workshop():
    return {
        "link_drive": LINK_DRIVE
    }


@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
