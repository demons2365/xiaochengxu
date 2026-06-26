import httpx
import json

BASE_URL = "http://localhost:8000"


def test_parse(text):
    """测试配置解析"""
    print(f"\n{'='*50}")
    print(f"测试解析: {text}")
    resp = httpx.post(f"{BASE_URL}/parse-config", json={"text": text})
    print(f"状态码: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"解析结果:")
        print(f"  CPU: {data.get('cpu', '')}")
        print(f"  GPU: {data.get('gpu', '')}")
        print(f"  内存: {data.get('ram', '')}")
        print(f"  SSD: {data.get('ssd', '')}")
        print(f"  HDD: {data.get('hdd', '')}")
        return data
    else:
        print(f"错误: {resp.text}")
        return None


def test_price(config):
    """测试价格计算"""
    print(f"\n{'='*50}")
    print(f"测试价格计算")
    resp = httpx.post(f"{BASE_URL}/calculate-price", json={"config": config})
    print(f"状态码: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"报价结果:")
        for item in data.get("items", []):
            print(f"  {item['name']}: {item['model']} -> {item['price']}")
        print(f"  ---")
        print(f"  总价: {data['total']}")
        return data
    else:
        print(f"错误: {resp.text}")
        return None


def test_lead():
    print(f"\n{'='*50}")
    print(f"测试提交留资")
    resp = httpx.post(f"{BASE_URL}/submit-lead", json={
        "phone": "13800138000",
        "wechat": "test_wechat",
        "config_text": "测试配置",
        "config_parsed": json.dumps({"test": True}),
        "price_total": 2330
    })
    print(f"状态码: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"结果: {data['message']}, ID: {data.get('lead_id')}")
    else:
        print(f"错误: {resp.text}")


if __name__ == "__main__":
    print("API 测试脚本")
    test_cases = [
        "i5 12400F + RTX4060 + 16G + 512G SSD",
        "i7 13700K 32G DDR5 1T固态 RTX4080",
        "R5 5600X RX6750XT 16G 512G固态",
        "i3 12100 8G 256G 办公电脑",
        "i9 14900K RTX4090 64G DDR5 2TB NVMe",
    ]
    for case in test_cases:
        config = test_parse(case)
        if config:
            test_price(config)
    test_lead()
    print(f"\n{'='*50}")
    print("测试完成！")
