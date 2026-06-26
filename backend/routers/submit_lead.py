# routers/submit_lead.py - 用户留资接口
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Lead
from schemas import SubmitLeadRequest, SubmitLeadResponse

router = APIRouter()


@router.post("/submit-lead", response_model=SubmitLeadResponse)
def api_submit_lead(req: SubmitLeadRequest, db: Session = Depends(get_db)):
    if not req.phone or not req.phone.strip():
        raise HTTPException(status_code=400, detail="请输入手机号")

    lead = Lead(
        phone=req.phone.strip(),
        wechat=req.wechat.strip(),
        config_text=req.config_text,
        config_parsed=req.config_parsed,
        price_total=req.price_total,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    return SubmitLeadResponse(success=True, message="提交成功", lead_id=lead.id)
