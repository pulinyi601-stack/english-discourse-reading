from fastapi import APIRouter
from ..schemas import TextCheckRequest, ApiResponse
from ..services.text_service import clean_text, is_valid_english, count_words, count_sentences, content_risk_check

router = APIRouter()

@router.post("/text/check", response_model=ApiResponse)
async def check_text(req: TextCheckRequest):
    raw = req.raw_text
    if not raw or not raw.strip():
        return {"code": 400, "msg": "文本不能为空", "data": {}}

    cleaned = clean_text(raw)
    valid = is_valid_english(cleaned)
    if not valid:
        return {"code": 200, "msg": "请求成功", "data": {
            "is_valid_english": False,
            "clean_text": cleaned,
            "word_count": 0,
            "sentence_count": 0,
            "risk_status": "pass",
            "risk_msg": ""
        }}

    wc = count_words(cleaned)
    sc = count_sentences(cleaned)
    risk, risk_msg = content_risk_check(cleaned)

    return {"code": 200, "msg": "请求成功", "data": {
        "is_valid_english": True,
        "clean_text": cleaned,
        "word_count": wc,
        "sentence_count": sc,
        "risk_status": risk,
        "risk_msg": risk_msg
    }}
