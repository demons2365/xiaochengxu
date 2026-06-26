# routers/submit_lead.py - ?????? + Server???
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Lead
from schemas import SubmitLeadRequest, SubmitLeadResponse
from config import SERVER_CHAN_KEY
import httpx

router = APIRouter()


def _send_server_chan(lead: Lead):
    if not SERVER_CHAN_KEY:
        return
    try:
        config_text = ""
        if lead.config_parsed:
            try:
                parsed = json.loads(lead.config_parsed)
                parts = []
                for k, v in parsed.items():
                    if v and k != "raw_items":
                        parts.append(f"{k}: {v}")
                config_text = " | ".join(parts)
            except:
                config_text = lead.config_parsed or ""

        title = "\u260e \u65b0\u7559\u8d44\u901a\u77e5 - \u00a5" + str(lead.price_total)
        lines = [
            "## \u65b0\u7684\u56de\u6536\u9884\u7ea6",
            "",
            "- **\u624b\u673a\u53f7**\uff1a" + (lead.phone or ""),
            "- **\u5fae\u4fe1**\uff1a" + (lead.wechat or "\u672a\u586b"),
            "- **\u62a5\u4ef7**\uff1a\u00a5" + str(lead.price_total),
            "- **\u539f\u59cb\u914d\u7f6e**\uff1a" + (lead.config_text or "\u65e0"),
            "- **\u8bc6\u522b\u7ed3\u679c**\uff1a" + (config_text or "\u65e0"),
            "- **\u65f6\u95f4**\uff1a" + (lead.create_time.strftime("%Y-%m-%d %H:%M") if lead.create_time else ""),
            "- **ID**\uff1a" + str(lead.id),
        ]
        desp = "\n".join(lines)

        url = "https://sct.ftqq.com/" + SERVER_CHAN_KEY + ".send"
        httpx.post(url, data={"title": title, "desp": desp}, timeout=10)
    except Exception as e:
        print("ServerChan \u53d1\u9001\u5931\u8d25:", e)


@router.post("/submit-lead", response_model=SubmitLeadResponse)
def api_submit_lead(req: SubmitLeadRequest, db: Session = Depends(get_db)):
    if not req.phone or not req.phone.strip():
        raise HTTPException(status_code=400, detail="\u8bf7\u8f93\u5165\u624b\u673a\u53f7")

    lead = Lead(
        phone=req.phone.strip(),
        wechat=req.wechat.strip(),
        config_text=req.config_text,
        config_parsed=req.config_parsed,
        price_total=req.price_total,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    _send_server_chan(lead)

    return SubmitLeadResponse(success=True, message="\u63d0\u4ea4\u6210\u529f", lead_id=lead.id)
