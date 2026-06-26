# init_db.py - 数据库初始化 + 种子数据
from database import engine, SessionLocal, Base
from models import PriceTable

Base.metadata.create_all(bind=engine)

seed_data = [
    # === CPU ===
    PriceTable(type="cpu", model="i3-12100", price=250, spec="4核8线程"),
    PriceTable(type="cpu", model="i3-12100F", price=200, spec="4核8线程"),
    PriceTable(type="cpu", model="i3-13100", price=350, spec="4核8线程"),
    PriceTable(type="cpu", model="i3-13100F", price=300, spec="4核8线程"),
    PriceTable(type="cpu", model="i5-12400F", price=450, spec="6核12线程"),
    PriceTable(type="cpu", model="i5-12400", price=500, spec="6核12线程"),
    PriceTable(type="cpu", model="i5-12490F", price=550, spec="6核12线程"),
    PriceTable(type="cpu", model="i5-12600K", price=700, spec="10核16线程"),
    PriceTable(type="cpu", model="i5-12600KF", price=650, spec="10核16线程"),
    PriceTable(type="cpu", model="i5-13400F", price=600, spec="10核16线程"),
    PriceTable(type="cpu", model="i5-13400", price=650, spec="10核16线程"),
    PriceTable(type="cpu", model="i5-13600K", price=1100, spec="14核20线程"),
    PriceTable(type="cpu", model="i5-13600KF", price=1050, spec="14核20线程"),
    PriceTable(type="cpu", model="i5-14400F", price=700, spec="10核16线程"),
    PriceTable(type="cpu", model="i5-14600K", price=1300, spec="14核20线程"),
    PriceTable(type="cpu", model="i5-14600KF", price=1250, spec="14核20线程"),
    PriceTable(type="cpu", model="i7-13700K", price=1700, spec="16核24线程"),
    PriceTable(type="cpu", model="i7-13700KF", price=1650, spec="16核24线程"),
    PriceTable(type="cpu", model="i7-14700K", price=1900, spec="20核28线程"),
    PriceTable(type="cpu", model="i7-14700KF", price=1850, spec="20核28线程"),
    PriceTable(type="cpu", model="i9-13900K", price=2400, spec="24核32线程"),
    PriceTable(type="cpu", model="i9-14900K", price=2700, spec="24核32线程"),
    PriceTable(type="cpu", model="Ultra 5 125H", price=600, spec="14核18线程"),
    PriceTable(type="cpu", model="Ultra 7 155H", price=900, spec="16核22线程"),
    PriceTable(type="cpu", model="Ultra 9 185H", price=1200, spec="16核22线程"),
    PriceTable(type="cpu", model="R5-4500", price=200, spec="6核12线程"),
    PriceTable(type="cpu", model="R5-5500", price=300, spec="6核12线程"),
    PriceTable(type="cpu", model="R5-5600", price=350, spec="6核12线程"),
    PriceTable(type="cpu", model="R5-5600X", price=400, spec="6核12线程"),
    PriceTable(type="cpu", model="R5-7500F", price=550, spec="6核12线程"),
    PriceTable(type="cpu", model="R5-7600", price=600, spec="6核12线程"),
    PriceTable(type="cpu", model="R5-7600X", price=650, spec="6核12线程"),
    PriceTable(type="cpu", model="R7-5700X", price=550, spec="8核16线程"),
    PriceTable(type="cpu", model="R7-5800X", price=650, spec="8核16线程"),
    PriceTable(type="cpu", model="R7-5800X3D", price=1200, spec="8核16线程"),
    PriceTable(type="cpu", model="R7-7700X", price=1000, spec="8核16线程"),
    PriceTable(type="cpu", model="R7-7800X3D", price=1800, spec="8核16线程"),
    PriceTable(type="cpu", model="R9-7950X", price=2500, spec="16核32线程"),

    # === GPU ===
    PriceTable(type="gpu", model="RTX 4060", price=1400, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RTX 4060 Ti", price=1800, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RTX 4070", price=2300, spec="12GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 4070 Super", price=2700, spec="12GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 4070 Ti", price=3000, spec="12GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 4080", price=4000, spec="16GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 4080 Super", price=4500, spec="16GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 4090", price=8000, spec="24GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 3060", price=1000, spec="12GB GDDR6"),
    PriceTable(type="gpu", model="RTX 3060 Ti", price=1200, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RTX 3070", price=1500, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RTX 3070 Ti", price=1700, spec="8GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 3080", price=2500, spec="10GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 3080 Ti", price=3200, spec="12GB GDDR6X"),
    PriceTable(type="gpu", model="RTX 3090", price=4000, spec="24GB GDDR6X"),
    PriceTable(type="gpu", model="GTX 1060", price=350, spec="6GB GDDR5"),
    PriceTable(type="gpu", model="GTX 1070", price=550, spec="8GB GDDR5"),
    PriceTable(type="gpu", model="GTX 1080", price=700, spec="8GB GDDR5X"),
    PriceTable(type="gpu", model="GTX 1080 Ti", price=1000, spec="11GB GDDR5X"),
    PriceTable(type="gpu", model="RTX 2060", price=700, spec="6GB GDDR6"),
    PriceTable(type="gpu", model="RTX 2070", price=900, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RTX 2080", price=1200, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RX 6600", price=800, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RX 6650 XT", price=1000, spec="8GB GDDR6"),
    PriceTable(type="gpu", model="RX 6750 XT", price=1200, spec="12GB GDDR6"),
    PriceTable(type="gpu", model="RX 6800", price=1500, spec="16GB GDDR6"),
    PriceTable(type="gpu", model="RX 7800 XT", price=2200, spec="16GB GDDR6"),
    PriceTable(type="gpu", model="RX 7900 XT", price=3500, spec="20GB GDDR6"),
    PriceTable(type="gpu", model="RX 7900 XTX", price=4200, spec="24GB GDDR6"),

    # === RAM ===
    PriceTable(type="ram", model="8GB DDR4", price=40, spec=""),
    PriceTable(type="ram", model="16GB DDR4", price=80, spec=""),
    PriceTable(type="ram", model="32GB DDR4", price=150, spec=""),
    PriceTable(type="ram", model="64GB DDR4", price=300, spec=""),
    PriceTable(type="ram", model="8GB DDR5", price=60, spec=""),
    PriceTable(type="ram", model="16GB DDR5", price=120, spec=""),
    PriceTable(type="ram", model="32GB DDR5", price=220, spec=""),
    PriceTable(type="ram", model="64GB DDR5", price=450, spec=""),

    # === SSD ===
    PriceTable(type="ssd", model="128GB SSD", price=30, spec=""),
    PriceTable(type="ssd", model="256GB SSD", price=60, spec=""),
    PriceTable(type="ssd", model="512GB SSD", price=120, spec=""),
    PriceTable(type="ssd", model="1TB SSD", price=200, spec=""),
    PriceTable(type="ssd", model="2TB SSD", price=350, spec=""),

    # === HDD ===
    PriceTable(type="hdd", model="500GB HDD", price=20, spec=""),
    PriceTable(type="hdd", model="1TB HDD", price=40, spec=""),
    PriceTable(type="hdd", model="2TB HDD", price=60, spec=""),
    PriceTable(type="hdd", model="4TB HDD", price=100, spec=""),
]


def init():
    init_if_empty()
def init_if_empty():
    """only seed when db empty"""
    db = SessionLocal()
    try:
        count = db.query(PriceTable).count()
        if count > 0:
            print(f"db has {count} records, skip")
            return
        for item in seed_data:
            db.add(item)
        db.commit()
        print(f"seeded {len(seed_data)} records")
    except Exception as e:
        db.rollback()
        print(f"seed error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init()
