from typing import Dict

from settings import logger_for

from fastapi import APIRouter, Depends

from .deps import decode_token

logger = logger_for(__name__)

router = APIRouter(prefix="/api/v1/public")


@router.get("/current_token", summary="Get the current token", response_model=Dict)
def get_current_token(token: Dict = Depends(decode_token)):
    return token
