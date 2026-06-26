# routers/admin.py - 后台管理 API
import os
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import PriceTable, Lead
from init_db import init_if_empty
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/admin", tags=["后台管理"])

# 简单 Token 认证
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
_admin_tokens = {}  # token -> expiry


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    message: str = ""


class PriceEntryCreate(BaseModel):
    type: str  # cpu/gpu/ram/ssd/hdd
    model: str
    price: float
    spec: str = ""


class BulkPriceEntry(BaseModel):
    entries: list[PriceEntryCreate]


class PriceEntryUpdate(BaseModel):
    model: Optional[str] = None
    price: Optional[float] = None
    spec: Optional[str] = None


def verify_token(authorization: str = Header("")):
    token = authorization.replace("Bearer ", "")
    if token not in _admin_tokens or _admin_tokens[token] < datetime.now():
        raise HTTPException(status_code=401, detail="未授权或登录已过期")
    return True


@router.post("/login", response_model=LoginResponse)
def admin_login(req: LoginRequest):
    if req.password != ADMIN_PASSWORD:
        return LoginResponse(success=False, message="密码错误")
    token = secrets.token_hex(32)
    _admin_tokens[token] = datetime.now() + timedelta(hours=8)
    return LoginResponse(success=True, token=token, message="登录成功")


# ============ 价格表管理 ============

@router.get("/price-table")
def list_prices(db: Session = Depends(get_db), _=Depends(verify_token)):
    prices = db.query(PriceTable).order_by(PriceTable.type, PriceTable.model).all()
    return [{
        "id": p.id,
        "type": p.type,
        "model": p.model,
        "price": p.price,
        "spec": p.spec or "",
    } for p in prices]


@router.post("/price-table")
def add_price(entry: PriceEntryCreate, db: Session = Depends(get_db), _=Depends(verify_token)):
    record = PriceTable(type=entry.type, model=entry.model, price=entry.price, spec=entry.spec)
    db.add(record)
    db.commit()
    return {"success": True, "id": record.id}
@router.post("/price-table/bulk")
def bulk_add_prices(bulk: BulkPriceEntry, db: Session = Depends(get_db), _=Depends(verify_token)):
    db.query(PriceTable).delete()
    for entry in bulk.entries:
        record = PriceTable(type=entry.type, model=entry.model, price=entry.price, spec=entry.spec)
        db.add(record)
    db.commit()
    count = db.query(PriceTable).count()
    return {"success": True, "message": f"已导入 {len(bulk.entries)} 条数据", "total": count}



@router.put("/price-table/{price_id}")
def update_price(price_id: int, entry: PriceEntryUpdate, db: Session = Depends(get_db), _=Depends(verify_token)):
    record = db.query(PriceTable).filter(PriceTable.id == price_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="未找到该记录")
    if entry.model is not None:
        record.model = entry.model
    if entry.price is not None:
        record.price = entry.price
    if entry.spec is not None:
        record.spec = entry.spec
    db.commit()
    return {"success": True}


@router.delete("/price-table/{price_id}")
def delete_price(price_id: int, db: Session = Depends(get_db), _=Depends(verify_token)):
    record = db.query(PriceTable).filter(PriceTable.id == price_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="未找到该记录")
    db.delete(record)
    db.commit()
    return {"success": True}


# ============ 留资管理 ============

@router.get("/leads")
def list_leads(db: Session = Depends(get_db), _=Depends(verify_token)):
    leads = db.query(Lead).order_by(Lead.create_time.desc()).all()
    return [{
        "id": l.id,
        "phone": l.phone,
        "wechat": l.wechat or "",
        "config_text": l.config_text or "",
        "config_parsed": l.config_parsed or "",
        "price_total": l.price_total or 0,
        "create_time": l.create_time.isoformat() if l.create_time else "",
    } for l in leads]


@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db), _=Depends(verify_token)):
    record = db.query(Lead).filter(Lead.id == lead_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="未找到该记录")
    db.delete(record)
    db.commit()
    return {"success": True}


# ============ 统计 ============

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _=Depends(verify_token)):
    total_prices = db.query(PriceTable).count()
    total_leads = db.query(Lead).count()
    today = datetime.now().date()
    today_leads = db.query(Lead).filter(Lead.create_time >= today).count()
    return {
        "total_prices": total_prices,
        "total_leads": total_leads,
        "today_leads": today_leads,
    }
