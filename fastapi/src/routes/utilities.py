from settings import logger_for
from worker.tasks import sum

from fastapi import APIRouter

logger = logger_for(__name__)

router = APIRouter(prefix="/api/v1/utilities")


@router.post("/sum")
def sum_operation(a: int, b: int):
    sum.delay(a, b)
    return {"message": "The sum task has been scheduled"}
