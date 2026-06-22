import re
import hashlib

def clean_text(raw: str) -> str:
    text = raw.strip()
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()

def is_valid_english(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return False
    words = text.split()
    alpha_count = sum(1 for w in words if re.search(r'[a-zA-Z]', w))
    return alpha_count >= max(3, len(words) * 0.3)

def count_words(text: str) -> int:
    return len([w for w in text.split() if w.strip()])

def count_sentences(text: str) -> int:
    sents = re.split(r'[.!?]+', text)
    return len([s for s in sents if s.strip()])

def content_risk_check(text: str) -> tuple:
    risk_keywords = [
        r'(?i)(?<![\w])sex(?![\w])', r'(?i)violence', r'(?i)porn',
        r'(?i)explicit', r'(?i)obscene', r'(?i)pornographic'
    ]
    for pattern in risk_keywords:
        if re.search(pattern, text):
            return "reject", "文本包含违规内容，无法生成报告"
    return "pass", ""

def text_hash(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()
