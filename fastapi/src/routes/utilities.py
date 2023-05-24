from settings import logger_for
from worker.tasks import multiply, sum

from fastapi import APIRouter

logger = logger_for(__name__)

router = APIRouter(prefix="/api/v1/utilities")


@router.post("/sum")
def sum_operation(a: int, b: int):
    sum.delay(a, b)
    return {"message": "The sum task has been scheduled"}


@router.post("/multiply")
def mutiply_operation(a: int, b: int):
    multiply.delay(a, b)
    return {"message": "The multiply task has been scheduled"}
