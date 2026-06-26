# services/price_engine.py - 价格查询引擎
from sqlalchemy.orm import Session
from models import PriceTable
from schemas import ParseConfigResponse, CalculatePriceResponse, PriceItem

# 模糊匹配映射表（简写 → 数据库中的标准型号）
GPU_ALIASES = {
    "4060": "RTX 4060",
    "4060ti": "RTX 4060 Ti",
    "4070": "RTX 4070",
    "4070ti": "RTX 4070 Ti",
    "4080": "RTX 4080",
    "4090": "RTX 4090",
    "3060": "RTX 3060",
    "3060ti": "RTX 3060 Ti",
    "3070": "RTX 3070",
    "3080": "RTX 3080",
    "3090": "RTX 3090",
    "2060": "RTX 2060",
    "2070": "RTX 2070",
    "2080": "RTX 2080",
    "1060": "GTX 1060",
    "1070": "GTX 1070",
    "1080": "GTX 1080",
    "6750": "RX 6750 XT",
    "6750xt": "RX 6750 XT",
    "6650": "RX 6650 XT",
    "6650xt": "RX 6650 XT",
    "6600": "RX 6600",
    "6800": "RX 6800",
    "6900xt": "RX 6900 XT",
    "7800xt": "RX 7800 XT",
    "7900xt": "RX 7900 XT",
    "7900xtx": "RX 7900 XTX",
}

CPU_ALIASES = {
    "12100": "i3-12100",
    "12100f": "i3-12100F",
    "13100": "i3-13100",
    "13100f": "i3-13100F",
    "12400": "i5-12400",
    "12400f": "i5-12400F",
    "12490f": "i5-12490F",
    "12600": "i5-12600",
    "12600k": "i5-12600K",
    "12600kf": "i5-12600KF",
    "13400": "i5-13400",
    "13400f": "i5-13400F",
    "13600": "i5-13600",
    "13600k": "i5-13600K",
    "13600kf": "i5-13600KF",
    "14600": "i5-14600",
    "14600k": "i5-14600K",
    "14600kf": "i5-14600KF",
    "13700": "i7-13700",
    "13700k": "i7-13700K",
    "14700": "i7-14700",
    "14700k": "i7-14700K",
    "14700kf": "i7-14700KF",
    "13900": "i9-13900",
    "13900k": "i9-13900K",
    "14900": "i9-14900",
    "14900k": "i9-14900K",
    "5600": "R5-5600",
    "5600x": "R5-5600X",
    "5700x": "R7-5700X",
    "5800x": "R7-5800X",
    "5800x3d": "R7-5800X3D",
    "7500f": "R5-7500F",
    "7600": "R5-7600",
    "7600x": "R5-7600X",
    "7700": "R7-7700",
    "7700x": "R7-7700X",
    "7800x3d": "R7-7800X3D",
    "7950x": "R9-7950X",
}

RAM_ALIASES = {
    "8g": "8GB",
    "16g": "16GB",
    "32g": "32GB",
    "64g": "64GB",
}


def _normalize_model(type_: str, model: str) -> str:
    """将用户输入的简写转为标准型号"""
    key = model.lower().replace(" ", "").replace("-", "")

    if type_ == "gpu":
        # 检查 GPU 别名
        for alias_key, standard in GPU_ALIASES.items():
            if alias_key in key:
                return standard
        # 如果已经是标准格式，清理空格
        return model.strip()

    if type_ == "cpu":
        for alias_key in sorted(CPU_ALIASES.keys(), key=len, reverse=True):
            if alias_key in key:
                return CPU_ALIASES[alias_key]
        return model.strip()

    if type_ == "ram":
        for alias_key, standard in RAM_ALIASES.items():
            if alias_key in key:
                return standard
        return model.strip()

    return model.strip()


def lookup_price(db: Session, type_: str, model: str) -> float:
    """在价格库中查询某个配件的价格"""
    normalized = _normalize_model(type_, model)

    # 精确匹配
    record = db.query(PriceTable).filter(
        PriceTable.type == type_,
        PriceTable.model == normalized
    ).first()
    if record:
        return record.price

    # 模糊匹配：模型包含
    record = db.query(PriceTable).filter(
        PriceTable.type == type_,
        PriceTable.model.like(f"%{normalized}%")
    ).first()
    if record:
        return record.price

    # 再模糊：别名匹配
    for alias_key, standard in {**GPU_ALIASES, **CPU_ALIASES}.items():
        if alias_key in model.lower().replace(" ", ""):
            record = db.query(PriceTable).filter(
                PriceTable.type == type_,
                PriceTable.model.like(f"%{standard}%")
            ).first()
            if record:
                return record.price

    return 0.0


def calculate_price(db: Session, config: ParseConfigResponse) -> CalculatePriceResponse:
    """根据解析结果计算总价"""
    items = []
    total = 0.0

    mappings = [
        ("cpu", config.cpu, "CPU"),
        ("gpu", config.gpu, "GPU"),
        ("ram", config.ram, "内存"),
        ("ssd", config.ssd, "固态硬盘"),
        ("hdd", config.hdd, "机械硬盘"),
    ]

    for type_, model, name in mappings:
        if not model:
            continue
        price = lookup_price(db, type_, model)
        items.append(PriceItem(name=name, model=_normalize_model(type_, model), price=price))
        total += price

    return CalculatePriceResponse(items=items, total=round(total, 2))
