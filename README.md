# 电脑回收自动估价系统 🖥️♻️

> 微信小程序 + FastAPI 后端，AI 智能识别电脑配置并自动估价

---

## 目录结构

`
computer-recycle-valuation/
├── backend/                          # FastAPI 后端
│   ├── main.py                       # 应用入口
│   ├── config.py                     # 配置文件
│   ├── database.py                   # 数据库连接
│   ├── models.py                     # ORM 模型
│   ├── schemas.py                    # Pydantic 模型
│   ├── init_db.py                    # 数据库初始化 + 种子数据
│   ├── requirements.txt              # Python 依赖
│   ├── test_api.py                   # API 测试脚本
│   ├── routers/
│   │   ├── parse_config.py           # POST /parse-config
│   │   ├── calculate_price.py        # POST /calculate-price
│   │   └── submit_lead.py            # POST /submit-lead
│   └── services/
│       ├── parser.py                 # AI/规则 配置解析引擎
│       └── price_engine.py           # 价格查询引擎
├── miniprogram/                      # 微信小程序
│   ├── app.js                        # 小程序入口
│   ├── app.json                      # 全局配置
│   ├── app.wxss                      # 全局样式
│   ├── sitemap.json
│   ├── images/                       # 图标资源
│   ├── pages/
│   │   ├── index/                    # 首页 - 输入配置
│   │   ├── result/                   # 结果页 - 报价明细
│   │   └── lead/                     # 留资页 - 联系方式
│   └── utils/
│       └── api.js                    # API 请求封装
└── README.md
`

---

## 🚀 快速启动

### 1. 后端启动

`ash
# 安装依赖
cd backend
pip install -r requirements.txt

# 初始化数据库（创建表 + 导入种子价格数据）
python init_db.py

# 启动服务
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
`

访问 http://localhost:8000/docs 查看 Swagger API 文档

### 2. 微信小程序启动

1. 打开 **微信开发者工具**
2. 导入 miniprogram/ 目录
3. 修改 pp.js 中的 piBaseUrl 为你的后端地址
   - 开发时：http://localhost:8000
   - 真机调试：改为电脑局域网IP（如 http://192.168.x.x:8000）
4. 在开发者工具中点击编译运行

> ⚠️ 小程序真机调试需要后端支持 HTTPS，开发阶段可以用「不校验合法域名」选项

---

## 🤖 AI 解析能力

系统支持 **两种解析模式**：

### 1. 规则解析（默认，无需配置）
内置正则引擎，支持解析：
- i5 12400F / R7 5800X / i7 13700K 等 CPU
- RTX4060 / RX6750XT / GTX1060 等 GPU
- 16G / 32GB DDR4 / 8G 等内存
- 512G SSD / 1T 固态 / 256G NVMe 等硬盘

### 2. LLM 解析（可选，更精准）
配置环境变量启用大模型解析：

`ash
# 设置你的 LLM API Key（OpenAI 兼容接口）
set LLM_API_KEY=sk-xxxxxxxx
set LLM_API_URL=https://api.openai.com/v1
set LLM_MODEL=gpt-4o-mini
`

启用后优先使用 LLM，失败自动回退到规则解析。

---

## 📡 API 接口说明

### 1. POST /parse-config — 解析配置

`json
// 请求
{ "text": "i5 12400F + RTX4060 + 16G + 512G SSD" }

// 响应
{
  "cpu": "i5-12400F",
  "gpu": "RTX4060",
  "ram": "16GB",
  "ssd": "512GB SSD",
  "hdd": ""
}
`

### 2. POST /calculate-price — 计算价格

`json
// 请求
{ "config": { "cpu": "i5-12400F", "gpu": "RTX4060", ... } }

// 响应
{
  "items": [
    { "name": "CPU", "model": "i5-12400F", "price": 450 },
    { "name": "GPU", "model": "RTX 4060", "price": 1400 },
    { "name": "内存", "model": "16GB", "price": 80 },
    { "name": "固态硬盘", "model": "512GB SSD", "price": 120 }
  ],
  "total": 2050
}
`

### 3. POST /submit-lead — 提交回收预约

`json
// 请求
{
  "phone": "13800138000",
  "wechat": "mywechat",
  "config_text": "i5 12400F + RTX4060 + 16G",
  "config_parsed": "{\"cpu\":\"...\"}",
  "price_total": 2050
}

// 响应
{ "success": true, "message": "提交成功", "lead_id": 1 }
`

---

## 🧪 测试

启动后端后，运行测试脚本：

`ash
cd backend
python test_api.py
`

测试用例覆盖：
- 5 组不同配置的解析 + 估价
- 1 组用户留资提交

---

## 🔧 自定义价格库

编辑 init_db.py 中的 seed_data 列表，按以下格式添加：

`python
PriceTable(type="cpu", model="型号", price=价格, spec="说明")
PriceTable(type="gpu", model="型号", price=价格, spec="说明")
PriceTable(type="ram", model="型号", price=价格, spec="说明")
PriceTable(type="ssd", model="型号", price=价格, spec="说明")
PriceTable(type="hdd", model="型号", price=价格, spec="说明")
`

修改后重新运行 python init_db.py 即可生效。

---

## 📊 数据库

使用 SQLite，文件为 ackend/recycle.db

### 表结构

**price_table** — 回收价格库
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| type | VARCHAR | cpu/gpu/ram/ssd/hdd |
| model | VARCHAR | 型号名称 |
| price | FLOAT | 回收单价 |
| spec | VARCHAR | 规格备注 |

**leads** — 用户留资
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| phone | VARCHAR | 手机号 |
| wechat | VARCHAR | 微信号 |
| config_text | TEXT | 原始输入 |
| config_parsed | TEXT | 解析结果 |
| price_total | FLOAT | 总价 |
| create_time | DATETIME | 提交时间 |

---

## 🔜 后续可扩展

- [ ] OCR 截图识别配置
- [ ] 用户登录/订单管理
- [ ] 工程师接单系统
- [ ] 微信支付集成
- [ ] 快递下单/上门回收
- [ ] 管理后台（价格库管理、订单管理）
- [ ] MySQL 迁移（生产环境）
