# models.py - SQLAlchemy ORM 模型
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class PriceTable(Base):
    __tablename__ = "price_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(20), nullable=False, comment="cpu / gpu / ram / ssd / hdd / motherboard / psu / case")
    model = Column(String(100), nullable=False, comment="型号名称")
    price = Column(Float, nullable=False, comment="回收单价(元)")
    spec = Column(String(200), default="", comment="规格备注")

    def __repr__(self):
        return f"<PriceTable(type={self.type}, model={self.model}, price={self.price})>"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String(20), nullable=False)
    wechat = Column(String(50), default="")
    config_text = Column(Text, default="", comment="用户原始输入")
    config_parsed = Column(Text, default="", comment="解析后的 JSON 字符串")
    price_total = Column(Float, default=0)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
