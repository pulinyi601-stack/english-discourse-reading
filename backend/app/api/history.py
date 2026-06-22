import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import HistoryRequest, ApiResponse
from ..models import HistoryRecord
from ..database import get_db

router = APIRouter()

@router.post("/history/operate", response_model=ApiResponse)
async def operate_history(req: HistoryRequest, db: Session = Depends(get_db)):
    op = req.operate_type

    if op == "list":
        if not req.user_token:
            return {"code": 200, "msg": "请求成功", "data": {"history_list": []}}
        records = db.query(HistoryRecord).filter(
            HistoryRecord.user_token == req.user_token,
            HistoryRecord.is_deleted == False
        ).order_by(HistoryRecord.create_time.desc()).limit(100).all()

        history = [{
            "task_id": r.task_id,
            "text_preview": r.text_preview or "未命名文本",
            "create_time": r.create_time.strftime("%Y-%m-%d %H:%M:%S") if r.create_time else "",
            "report_preview": r.report_preview or ""
        } for r in records]

        return {"code": 200, "msg": "请求成功", "data": {"history_list": history}}

    elif op == "add":
        record = HistoryRecord(
            task_id=req.task_id or f"hist_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            user_token=req.user_token or "",
            text_preview="",
            report_preview="",
            create_time=datetime.datetime.utcnow()
        )
        db.add(record)
        db.commit()
        return {"code": 200, "msg": "保存成功", "data": {"operate_result": True}}

    elif op == "delete":
        db.query(HistoryRecord).filter(
            HistoryRecord.task_id == req.task_id
        ).update({"is_deleted": True})
        db.commit()
        return {"code": 200, "msg": "删除成功", "data": {"operate_result": True}}

    elif op == "clear":
        db.query(HistoryRecord).filter(
            HistoryRecord.user_token == req.user_token
        ).update({"is_deleted": True})
        db.commit()
        return {"code": 200, "msg": "已清空", "data": {"operate_result": True}}

    return {"code": 400, "msg": "无效的操作类型", "data": {}}
