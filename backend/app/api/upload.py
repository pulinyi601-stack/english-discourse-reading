from fastapi import APIRouter, UploadFile, File, HTTPException
from ..schemas import ApiResponse
from ..services.file_service import validate_file, extract_text_from_file
import aiofiles
import tempfile
import os

router = APIRouter()

@router.post("/file/upload", response_model=ApiResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        return {"code": 400, "msg": "请选择要上传的文件", "data": {}}

    content = await file.read()
    valid, msg = validate_file(file.filename, len(content))
    if not valid:
        return {"code": 400, "msg": msg, "data": {}}

    success, result = await extract_text_from_file(file.filename, content)
    if not success:
        return {"code": 400, "msg": result, "data": {}}

    return {"code": 200, "msg": "文件解析成功", "data": {
        "filename": file.filename,
        "text_content": result,
        "word_count": len(result.split()),
        "char_count": len(result)
    }}
