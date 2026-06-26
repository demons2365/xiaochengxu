# main.py - FastAPI 应用入口
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from fastapi.staticfiles import StaticFiles
from init_db import init_if_empty
from routers import parse_config, calculate_price, submit_lead, admin
from models import PriceTable, Lead  # noqa: ensure models are imported

# 创建所有表
Base.metadata.create_all(bind=engine)
# auto seed on startup
init_if_empty()

app = FastAPI(
    title="电脑回收估价系统 API",
    description="自动识别电脑配置并估价",
    version="1.0.0",
)

# CORS 允许小程序访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(parse_config.router, tags=["配置解析"])
app.include_router(calculate_price.router, tags=["价格计算"])
app.include_router(submit_lead.router, tags=["用户留资"])
app.include_router(admin.router)

# 挂载静态文件（优先级最低，仅用于首页预览）
try:
    import os
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.isdir(static_dir):
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
except Exception as e:
    print(f"Static mount skipped: {e}")


@app.get("/")
def root():
    return {"message": "电脑回收估价系统 API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
