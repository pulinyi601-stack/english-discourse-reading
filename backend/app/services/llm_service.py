import json
import httpx
from ..config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL

SYSTEM_PROMPT = """你是一位专业的中国高中英语教研员。请严格按照 What-Why-How 三层结构分析以下英文语篇，生成中文研读报告。

报告必须包含以下6个模块，缺一不可：

## 一、文本基础信息 (What)
- 文本主题
- 核心内容概括
- 段落大意拆分

## 二、写作意图分析 (Why)
- 作者写作目的
- 情感态度
- 核心观点
- 文本育人价值（贴合高中英语课标）

## 三、文本写法分析 (How)
- 文体结构判定（记叙文/议论文/说明文/新闻）
- 行文逻辑
- 句式特点
- 修辞分析
- 重难点词汇 & 长难句标注

## 四、教学重难点
## 五、阅读命题切入点
## 六、课堂教学设计建议

要求：
1. 所有分析必须绑定原文语句，使用引号标注
2. 重难点词汇标注CEFR等级（A1-C2）
3. 使用Markdown格式输出
4. 贴合中国高中英语教学实际
5. 分析要具体，避免空泛评价"""

async def call_deepseek(text: str, genre: str = "auto") -> str:
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_api_key_here":
        return _generate_mock_report(text, genre)

    user_prompt = f"""请分析以下英文语篇（文体类型：{genre}）：

{text}

请严格按照6模块格式输出完整研读报告。"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

def detect_genre(text: str) -> str:
    text_lower = text[:500].lower()
    narrative = ["once upon a time", "i remember", "last year", "one day", "when i was"]
    argumentative = ["argue", "believe", "should", "however", "in my opinion", "therefore"]
    expository = ["is defined as", "refers to", "consists of", "for example", "such as"]
    news = ["reported that", "according to", "announced", "yesterday", "officials said"]

    def score(keywords):
        return sum(1 for k in keywords if k in text_lower)

    scores = {
        "记叙文": score(narrative),
        "议论文": score(argumentative),
        "说明文": score(expository),
        "新闻": score(news)
    }
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "说明文"

def _generate_mock_report(text: str, genre: str) -> str:
    preview = text[:100].strip()
    return f"""# 语篇深度研读报告

## 一、文本基础信息 (What)

### 文本主题
本文围绕 "{preview}..." 展开，主题聚焦于该语篇所传达的核心内容。

### 核心内容概括
本文主要探讨了与主题相关的关键信息，通过具体事例和细节描述使读者对相关内容形成全面认识。

### 段落大意拆分
- **第1段**：引入主题，提出背景信息
- **第2段**：展开论述，提供具体论据或细节
- **第3段**：总结观点，得出结论或展望

## 二、写作意图分析 (Why)

### 作者写作目的
作者旨在向读者介绍/阐释相关主题，帮助读者建立对该主题的系统认知。

### 情感态度
作者以客观中立的态度进行论述，通过事实和证据支撑观点，体现了严谨的写作风格。

### 核心观点
文章强调了 "{preview[:50]}..." 这一核心论点，并围绕该论点展开深入分析。

### 文本育人价值
该语篇符合高中英语课标要求，有助于培养学生的跨文化意识、批判性思维能力和语言综合运用能力。

## 三、文本写法分析 (How)

### 文体结构判定
本文为**{genre}**，结构清晰，逻辑严谨。

### 行文逻辑
文章采用"总-分-总"结构，从概括到具体再到总结，逻辑链条完整。

### 句式特点
文中包含复合句、定语从句、状语从句等多种句式，丰富了表达的层次感。

### 修辞分析
作者运用了排比、对比等修辞手法，增强了文本的表现力和说服力。

### 重难点词汇 & 长难句标注
- **重点词汇**：均属于高中英语核心词汇范畴
- **长难句分析**：文中包含多重复合结构的长句，需引导学生进行句子成分分析

## 四、教学重难点
- **重点**：理解文章主旨大意，掌握核心词汇和关键句型
- **难点**：分析长难句结构，理解作者隐含的观点态度

## 五、阅读命题切入点
- 主旨大意题：考查学生对全文主题的把握
- 细节理解题：考查对具体信息的定位和理解能力
- 推理判断题：考查基于文本信息的逻辑推理能力
- 词义猜测题：考查根据上下文推断词义的能力

## 六、课堂教学设计建议
1. **导入环节**：通过图片/视频引入主题，激活学生背景知识
2. **泛读环节**：快速阅读，概括段落大意
3. **精读环节**：分析长难句，解读深层含义
4. **读后活动**：小组讨论，联系实际，拓展思维
5. **作业布置**：仿写相关主题短文，巩固语言知识
"""
