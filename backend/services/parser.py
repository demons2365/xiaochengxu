# services/parser.py - 智能硬件配置解析器
# 支持两种解析模式：
# 1. 规则解析（默认） - 基于正则表达式匹配常见硬件格式
# 2. LLM解析（可选） - 调用大模型API，需配置 LLM_API_KEY

import re
import json
from typing import Optional
from config import LLM_API_KEY, LLM_API_URL, LLM_MODEL

from schemas import ParseConfigResponse, HardwareItem


def _clean_text(text: str) -> str:
    text = text.replace("\uff0b", "+").replace("\uff0c", ",").replace("\u3000", " ")
    return text.strip()


def _find_cpu(text: str) -> str:
    patterns = [
        r"(?:Intel\s*)?(?:Core\s*)?(?:i[3579]-?\d{4,5}[A-Za-z0-9]*[FKSHT]{0,3})",
        r"(?:Intel\s*)?(?:Core\s*)?(?:Ultra\s*\d{1,2}\s*\d{3}[A-Za-z0-9]*)",
        r"(?:AMD\s*)?(?:Ryzen\s*)?(?:R\d\s*\d{4}[A-Za-z0-9]*)",
        r"(?:AMD\s*)?(?:Ryzen\s*)?(?:R\d\s*\d{3}[A-Za-z0-9]*)",
        r"(?:i[3579]\s*\d{4,5}[A-Za-z0-9]*)",
        r"(?:R[579]\s*\d{4}[A-Za-z0-9]*)",
        r"(?:Xeon\s*\S+)",
        r"(?:EPYC\s*\S+)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return ""


def _find_gpu(text: str) -> str:
    patterns = [
        r"(?:NVIDIA\s*)?(?:GeForce\s*)?(?:RTX\s*\d{4}\s*[A-Za-z0-9]*)",
        r"(?:NVIDIA\s*)?(?:GeForce\s*)?(?:GTX\s*\d{4}\s*[A-Za-z0-9]*)",
        r"(?:NVIDIA\s*)?(?:GeForce\s*)?(?:GT\s*\d{3,4})",
        r"(?:AMD\s*)?(?:Radeon\s*)?(?:RX\s*\d{4}\s*[A-Za-z0-9]*)",
        r"(?:AMD\s*)?(?:Radeon\s*)?(?:RX\s*\d{3}\s*[A-Za-z0-9]*)",
        r"(?:Intel\s*)?(?:Arc\s*)?(?:A\d{3})",
        r"(?:RTX\s*\d{4}[A-Za-z0-9]*)",
        r"(?:GTX\s*\d{4}[A-Za-z0-9]*)",
        r"(?:RX\s*\d{4}[A-Za-z0-9]*)",
        r"(?:RX\s*\d{3}[A-Za-z0-9]*)",
        r"(?<!\d)(?:40[6789]0)(?:Ti|S|D|SUPER)?(?!\d)",
        r"(?<!\d)(?:30[56789]0)(?:Ti|S)?(?!\d)",
        r"(?<!\d)(?:20[6789]0)(?:Ti|S|SUPER)?(?!\d)",
        r"(?<!\d)(?:10[6789]0)(?:Ti)?(?!\d)",
        r"(?<!\d)(?:6[56789]50)(?:XT)?(?!\d)",
        r"(?<!\d)(?:6[6789]00)(?:XT)?(?!\d)",
        r"(?<!\d)(?:7[56789]00)(?:XT|XTX|GRE)?(?!\d)",
        r"(?<!\d)(?:5[6789]00)(?:XT)?(?!\d)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            result = m.group(0).strip()
            # Remove trailing digits from other components
            result = re.sub(r"\s+\d+[Gg][Bb]?$", "", result)
            return result
    return ""


def _find_ram(text: str) -> str:
    # Match patterns like: 16G, 32GB, 16GB DDR4, 8G DDR3, 2x8G
    m = re.search(r"(?<!\d)(\d+)\s*(?:[xX*]\s*\d+\s*)?(?:G|GB)\s*(?:DDR[345])?", text, re.IGNORECASE)
    if m:
        # Find the total capacity
        cap_m = re.search(r"(?<!\d)(\d+)\s*(?:G|GB)\s*(?:DDR[345])?", text, re.IGNORECASE)
        if cap_m:
            size = cap_m.group(1)
            ddr = ""
            ddr_m = re.search(r"(DDR[345])", text, re.IGNORECASE)
            if ddr_m:
                ddr = ddr_m.group(1)
            return f"{size}GB {ddr}" if ddr else f"{size}GB"
    return ""


def _find_ssd(text: str) -> str:
    # Must have explicit SSD/固态/NVMe keyword
    m = re.search(r"(?<!\d)(\d+)\s*(?:G|GB|T|TB)\s*(?:SSD|固态|NVMe|M\.\s*2)", text, re.IGNORECASE)
    if m:
        size = m.group(1)
        unit = "GB"
        raw = text[m.start():m.end()]
        if re.search(r"[Tt]", raw):
            unit = "TB"
        return f"{size}{unit} SSD"
    return ""


def _find_hdd(text: str) -> str:
    m = re.search(r"(?<!\d)(\d+)\s*(?:G|GB|T|TB)\s*(?:HDD|机械|硬盘)", text, re.IGNORECASE)
    if m:
        size = m.group(1)
        unit = "GB"
        raw = text[m.start():m.end()]
        if re.search(r"[Tt]", raw):
            unit = "TB"
        return f"{size}{unit} HDD"
    return ""


def rule_parse(text: str) -> ParseConfigResponse:
    text = _clean_text(text)
    cpu = _find_cpu(text)
    gpu = _find_gpu(text)
    ram = _find_ram(text)
    ssd = _find_ssd(text)
    hdd = _find_hdd(text)

    raw_items = []
    if cpu:
        raw_items.append(HardwareItem(type="cpu", model=cpu, raw=cpu))
    if gpu:
        raw_items.append(HardwareItem(type="gpu", model=gpu, raw=gpu))
    if ram:
        raw_items.append(HardwareItem(type="ram", model=ram, raw=ram))
    if ssd:
        raw_items.append(HardwareItem(type="ssd", model=ssd, raw=ssd))
    if hdd:
        raw_items.append(HardwareItem(type="hdd", model=hdd, raw=hdd))

    return ParseConfigResponse(
        cpu=cpu, gpu=gpu, ram=ram, ssd=ssd, hdd=hdd, raw_items=raw_items,
    )


async def llm_parse(text: str) -> Optional[ParseConfigResponse]:
    if not LLM_API_KEY:
        return None
    try:
        import httpx
        prompt = (
            f"You are a hardware parsing expert. Extract computer specs from this input.\n\n"
            f'Input: "{text}"\n\n'
            f"Extract:\n1. CPU (e.g. i5-12400F, R7-5800X)\n"
            f"2. GPU (e.g. RTX4060, RX6750XT)\n"
            f"3. RAM (e.g. 16GB DDR4, 32GB)\n"
            f"4. SSD (e.g. 512GB SSD, 1TB NVMe)\n"
            f"5. HDD (e.g. 1TB HDD)\n\n"
            f"Return ONLY JSON:\n"
            f'{{"cpu":"...","gpu":"...","ram":"...","ssd":"...","hdd":"..."}}\n'
            f"Use empty string for missing fields."
        )
        headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
        body = {"model": LLM_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{LLM_API_URL}/chat/completions", json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group(0))
            raw_items = [HardwareItem(type=k, model=v, raw=v) for k, v in parsed.items() if v]
            return ParseConfigResponse(
                cpu=parsed.get("cpu", ""), gpu=parsed.get("gpu", ""),
                ram=parsed.get("ram", ""), ssd=parsed.get("ssd", ""),
                hdd=parsed.get("hdd", ""), raw_items=raw_items,
            )
    except Exception as e:
        print(f"[LLM Parse Error] {e}")
    return None


async def parse_config(text: str) -> ParseConfigResponse:
    result = await llm_parse(text)
    if result:
        return result
    return rule_parse(text)
