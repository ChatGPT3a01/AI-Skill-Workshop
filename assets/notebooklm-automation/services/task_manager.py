"""背景任務管理"""
import threading
import uuid
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    """任務狀態"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Task:
    """任務類別"""

    def __init__(self, task_id: str, name: str, func: Callable, args: tuple = (), kwargs: dict = None):
        self.id = task_id
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.progress = 0

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class TaskManager:
    """任務管理器"""

    def __init__(self, max_workers: int = 5):
        self.tasks: Dict[str, Task] = {}
        self.max_workers = max_workers
        self._lock = threading.Lock()

    def create_task(self, name: str, func: Callable, args: tuple = (), kwargs: dict = None) -> str:
        """建立新任務"""
        task_id = str(uuid.uuid4())[:8]
        task = Task(task_id, name, func, args, kwargs)

        with self._lock:
            self.tasks[task_id] = task

        # 啟動任務執行緒
        thread = threading.Thread(target=self._run_task, args=(task_id,))
        thread.daemon = True
        thread.start()

        return task_id

    def _run_task(self, task_id: str):
        """執行任務"""
        task = self.tasks.get(task_id)
        if not task:
            return

        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()

            # 執行任務函式
            result = task.func(*task.args, **task.kwargs)

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.progress = 100
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
        finally:
            task.completed_at = datetime.now()

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """取得任務狀態"""
        task = self.tasks.get(task_id)
        if task:
            return task.to_dict()
        return None

    def get_all_tasks(self) -> list:
        """取得所有任務"""
        return [task.to_dict() for task in self.tasks.values()]

    def update_progress(self, task_id: str, progress: int):
        """更新任務進度"""
        task = self.tasks.get(task_id)
        if task:
            task.progress = min(100, max(0, progress))

    def cancel_task(self, task_id: str) -> bool:
        """取消任務（僅限尚未開始的任務）"""
        task = self.tasks.get(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.FAILED
            task.error = "已取消"
            return True
        return False

    def clean_old_tasks(self, max_age_hours: int = 24):
        """清理舊任務"""
        now = datetime.now()
        with self._lock:
            to_remove = []
            for task_id, task in self.tasks.items():
                if task.completed_at:
                    age = (now - task.completed_at).total_seconds() / 3600
                    if age > max_age_hours:
                        to_remove.append(task_id)
            for task_id in to_remove:
                del self.tasks[task_id]


# 建立單例
task_manager = TaskManager()
