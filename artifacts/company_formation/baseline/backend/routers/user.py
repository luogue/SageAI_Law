"""用户相关路由"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.routes import get_current_user
from storage.crud import get_user_bonus_credits

router = APIRouter(prefix="/user", tags=["user"])


class CreditsResponse(BaseModel):
    bonus_credits: int


@router.get("/credits", response_model=CreditsResponse)
async def get_user_credits(user_id: int = Depends(get_current_user)):
    """获取用户剩余免费额度"""
    credits = get_user_bonus_credits(user_id)
    return {"bonus_credits": credits}
