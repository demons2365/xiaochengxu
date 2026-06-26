# routers/parse_config.py - 配置解析接口
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ParseConfigRequest, ParseConfigResponse
from services.parser import parse_config

router = APIRouter()


@router.post("/parse-config", response_model=ParseConfigResponse)
async def api_parse_config(req: ParseConfigRequest, db: Session = Depends(get_db)):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="请输入电脑配置信息")

    result = await parse_config(req.text.strip())
    return result
