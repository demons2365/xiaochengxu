# schemas.py - Pydantic 请求/响应模型
from pydantic import BaseModel
from typing import Optional


class ParseConfigRequest(BaseModel):
    text: str


class HardwareItem(BaseModel):
    type: str  # cpu / gpu / ram / ssd / hdd
    model: str
    raw: str = ""


class ParseConfigResponse(BaseModel):
    cpu: str = ""
    gpu: str = ""
    ram: str = ""
    ssd: str = ""
    hdd: str = ""
    raw_items: list[HardwareItem] = []


class PriceItem(BaseModel):
    name: str
    model: str
    price: float


class CalculatePriceRequest(BaseModel):
    config: ParseConfigResponse


class CalculatePriceResponse(BaseModel):
    items: list[PriceItem] = []
    total: float = 0


class SubmitLeadRequest(BaseModel):
    phone: str
    wechat: str = ""
    config_text: str = ""
    config_parsed: str = ""
    price_total: float = 0


class SubmitLeadResponse(BaseModel):
    success: bool = True
    message: str = "提交成功"
    lead_id: Optional[int] = None
