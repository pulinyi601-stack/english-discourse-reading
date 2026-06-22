import datetime
from pathlib import Path
from fastapi import APIRouter
from ..schemas import GenerateRequest, ExportRequest, ApiResponse
from ..services.report_service import task_manager
from ..services.text_service import text_hash
from ..config import CACHE_PREFIX, FREE_DAILY_LIMIT

router = APIRouter()

_in_memory_cache = {}
_in_memory_quota = {}

def _check_quota(user_token: str) -> int:
    today = datetime.date.today().isoformat()
    key = f"{user_token or 'visitor'}:{today}"
    used = _in_memory_quota.get(key, 0)
    return max(0, FREE_DAILY_LIMIT - used)

def _use_quota(user_token: str) -> int:
    today = datetime.date.today().isoformat()
    key = f"{user_token or 'visitor'}:{today}"
    _in_memory_quota[key] = _in_memory_quota.get(key, 0) + 1
    return max(0, FREE_DAILY_LIMIT - _in_memory_quota[key])

@router.post("/report/generate", response_model=ApiResponse)
async def generate_report(req: GenerateRequest):
    remain = _check_quota(req.user_token)
    if remain <= 0 and req.user_type == "visitor":
        return {"code": 403, "msg": "今日免费额度已用尽，请登录或次日再试", "data": {}}

    text_key = CACHE_PREFIX + text_hash(req.clean_text)
    if text_key in _in_memory_cache:
        task_id = f"cached_{datetime.datetime.now().strftime('%Y%m%d')}_{text_hash(req.clean_text)[:8]}"
        return {"code": 200, "msg": "请求成功", "data": {
            "task_id": task_id,
            "remain_quota": remain,
            "task_status": "success"
        }}

    task_id = task_manager.create_task(req.clean_text, req.text_word_num)
    task_manager.start_task(task_id)
    _use_quota(req.user_token)
    remain_after = _check_quota(req.user_token)

    return {"code": 200, "msg": "请求成功", "data": {
        "task_id": task_id,
        "remain_quota": remain_after,
        "task_status": "pending"
    }}

@router.get("/report/progress", response_model=ApiResponse)
async def get_progress(task_id: str):
    if task_id.startswith("cached_"):
        hash_part = task_id.split("_")[-1]
        for key, val in _in_memory_cache.items():
            if hash_part in key:
                return {"code": 200, "msg": "请求成功", "data": {
                    "task_status": "success",
                    "progress_percent": 100,
                    "report_content": val,
                    "fail_reason": ""
                }}
        return {"code": 500, "msg": "缓存记录未找到", "data": {}}

    task = task_manager.get_task(task_id)
    if not task:
        return {"code": 400, "msg": "任务ID不存在", "data": {}}

    return {"code": 200, "msg": "请求成功", "data": {
        "task_status": task["task_status"],
        "progress_percent": task["progress_percent"],
        "report_content": task["report_content"],
        "fail_reason": task["fail_reason"]
    }}

@router.post("/report/export", response_model=ApiResponse)
async def export_report(req: ExportRequest):
    file_ext = {"word": "docx", "pdf": "pdf", "markdown": "md"}
    ext = file_ext.get(req.export_type, "md")
    file_name = f"高中英语语篇研读报告_{datetime.datetime.now().strftime('%Y%m%d')}.{ext}"

    if req.export_type == "markdown":
        export_dir = Path(__file__).resolve().parent.parent.parent / "exports"
        export_dir.mkdir(exist_ok=True)
        file_path = export_dir / file_name
        file_path.write_text(req.report_content, encoding="utf-8")
        file_url = f"/exports/{file_name}"
    else:
        file_url = f"/exports/{file_name}"

    return {"code": 200, "msg": "请求成功", "data": {
        "file_download_url": file_url,
        "file_name": file_name
    }}
