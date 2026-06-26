# routers/calculate_price.py - 价格计算接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import CalculatePriceRequest, CalculatePriceResponse
from services.price_engine import calculate_price

router = APIRouter()


@router.post("/calculate-price", response_model=CalculatePriceResponse)
def api_calculate_price(req: CalculatePriceRequest, db: Session = Depends(get_db)):
    if not req.config:
        raise HTTPException(status_code=400, detail="请先解析配置")

    result = calculate_price(db, req.config)
    return result
