import uuid
import datetime
import asyncio
from typing import Optional, Dict

from ..config import TIMEOUT_SHORT, TIMEOUT_MEDIUM, TIMEOUT_LONG
from .llm_service import call_deepseek, detect_genre

class TaskManager:
    def __init__(self):
        self._tasks: Dict[str, dict] = {}

    def create_task(self, clean_text: str, word_count: int) -> str:
        task_id = f"task_{datetime.datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4().hex[:6])}"
        timeout = self._get_timeout(word_count)

        self._tasks[task_id] = {
            "task_id": task_id,
            "task_status": "pending",
            "progress_percent": 0,
            "report_content": "",
            "fail_reason": "",
            "clean_text": clean_text,
            "word_count": word_count,
            "timeout": timeout,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        return task_id

    def _get_timeout(self, word_count: int) -> int:
        if word_count <= 1000:
            return TIMEOUT_SHORT
        elif word_count <= 3000:
            return TIMEOUT_MEDIUM
        else:
            return TIMEOUT_LONG

    async def execute_task(self, task_id: str):
        task = self._tasks.get(task_id)
        if not task:
            return

        try:
            task["progress_percent"] = 10
            await asyncio.sleep(0.5)

            genre = detect_genre(task["clean_text"])
            task["progress_percent"] = 20

            report = await call_deepseek(task["clean_text"], genre)
            task["progress_percent"] = 90

            task["report_content"] = report
            task["task_status"] = "success"
            task["progress_percent"] = 100

        except asyncio.TimeoutError:
            task["task_status"] = "fail"
            task["fail_reason"] = "生成超时，请稍后重试"
        except Exception as e:
            task["task_status"] = "fail"
            task["fail_reason"] = f"生成失败：{str(e)}"

    def get_task(self, task_id: str) -> Optional[dict]:
        return self._tasks.get(task_id)

    def start_task(self, task_id: str):
        task = self._tasks.get(task_id)
        if task:
            asyncio.create_task(self.execute_task(task_id))

task_manager = TaskManager()
