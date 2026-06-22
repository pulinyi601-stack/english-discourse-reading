import io
from pathlib import Path

ALLOWED_EXTENSIONS = {
    '.txt': 'text/plain',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.pdf': 'application/pdf',
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file(filename: str, content_length: int) -> tuple[bool, str]:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"不支持的文件格式：{ext}，支持 txt/docx/pdf"
    if content_length > MAX_FILE_SIZE:
        return False, "文件大小超过 10MB 限制"
    return True, ""


async def extract_text_from_file(filename: str, content: bytes) -> tuple[bool, str]:
    ext = Path(filename).suffix.lower()

    try:
        if ext == '.txt':
            return True, content.decode('utf-8', errors='replace')

        elif ext == '.docx':
            return _extract_docx(content)

        elif ext == '.pdf':
            return _extract_pdf(content)

        return False, "不支持的文件格式"
    except Exception as e:
        return False, f"文件解析失败：{str(e)}"


def _extract_docx(content: bytes) -> tuple[bool, str]:
    from docx import Document
    doc = Document(io.BytesIO(content))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return True, '\n\n'.join(paragraphs)


def _extract_pdf(content: bytes) -> tuple[bool, str]:
    import fitz
    doc = fitz.open(stream=content, filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            pages.append(text)
    doc.close()
    return True, '\n\n'.join(pages)
