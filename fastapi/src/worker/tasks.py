from settings import logger_for

logger = logger_for(__name__)

from celery import current_app as app


@app.task
def sum(x, y):
    r = x + y
    logger.info(f"Sum result: {r}")
    return r
