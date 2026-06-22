from pydantic import BaseModel
from typing import Optional, List

class TextCheckRequest(BaseModel):
    raw_text: str
    user_type: str  # visitor / login

class TextCheckResponse(BaseModel):
    is_valid_english: bool
    clean_text: str
    word_count: int
    sentence_count: int
    risk_status: str  # pass / reject
    risk_msg: str

class GenerateRequest(BaseModel):
    clean_text: str
    text_word_num: int
    user_token: Optional[str] = ""
    user_type: str = "visitor"

class GenerateResponse(BaseModel):
    task_id: str
    remain_quota: int
    task_status: str

class ProgressResponse(BaseModel):
    task_status: str
    progress_percent: int
    report_content: Optional[str] = ""
    fail_reason: Optional[str] = ""

class ExportRequest(BaseModel):
    task_id: str
    export_type: str  # word / pdf / markdown
    report_content: str

class ExportResponse(BaseModel):
    file_download_url: str
    file_name: str

class HistoryRequest(BaseModel):
    operate_type: str  # add / list / delete / clear
    task_id: Optional[str] = ""
    user_token: Optional[str] = ""

class HistoryItem(BaseModel):
    task_id: str
    text_preview: str
    create_time: str
    report_preview: str

class HistoryResponse(BaseModel):
    history_list: List[HistoryItem] = []
    operate_result: Optional[bool] = None

class ApiResponse(BaseModel):
    code: int
    msg: str
    data: dict
