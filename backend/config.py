# config.py - 全局配置
import os

# 数据库连接：优先读取环境变量（CloudBase 会自动注入）
# MySQL 连接格式：mysql+pymysql://root:xxx@host:port/db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recycle.db")

# LLM API 配置（可选，未配置时使用规则解析器）
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# 小程序 AppID（发布时填写）
WECHAT_APP_ID = os.getenv("WECHAT_APP_ID", "your_app_id")

# CloudBase Cloud Run 配置——如果没有 DATABASE_URL 但有 CloudBase 提供的 MySQL 环境变量，则自动组装
_MYSQL_HOST = os.getenv("MYSQL_HOST") or os.getenv("MYSQL_HOSTNAME")
_MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
_MYSQL_USER = os.getenv("MYSQL_USER") or os.getenv("MYSQL_USERNAME", "root")
_MYSQL_PASS = os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQL_INSTANCE_PASSWORD")
_MYSQL_DB = os.getenv("MYSQL_DATABASE") or os.getenv("MYSQL_INSTANCE_NAME", "recycle")

if _MYSQL_HOST and _MYSQL_PASS and DATABASE_URL.startswith("sqlite"):
    DATABASE_URL = f"mysql+pymysql://{_MYSQL_USER}:{_MYSQL_PASS}@{_MYSQL_HOST}:{_MYSQL_PORT}/{_MYSQL_DB}?charset=utf8mb4"
