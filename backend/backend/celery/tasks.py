from backend.celery.worker import celery
from typing import List


def getTasksStatus(tasks_id: List[str]):
    result = []
    for task_id in tasks_id:
        task_result = celery.AsyncResult(task_id)
        result.append({
            "task_id": task_id,
            "task_status": task_result.status,
        })
    return result

def getTaskResult(task_id: str):
    task_result = celery.AsyncResult(task_id)
    return {
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    
def deleteTasks(tasks_id: List[str]):
    celery.control.revoke(tasks_id, terminate = True)