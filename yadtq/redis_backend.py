import redis
from .config import REDIS_CONFIG

redis_client = redis.StrictRedis(**REDIS_CONFIG)

def set_task_status(task_id, status, worker_id=None, result=None, error=None):
    redis_client.hset(task_id, "status", status)
    if worker_id:
        redis_client.hset(task_id, "worker_id", worker_id)
    if result:
        redis_client.hset(task_id, "result", result)
    if error:
        redis_client.hset(task_id, "error", error)

def query_all_tasks():
    task_ids = redis_client.keys("*")
    tasks = []
    for task_id in task_ids:
        if redis_client.type(task_id) == 'hash':
            task_data = redis_client.hgetall(task_id)
            tasks.append({
                "task_id": task_id,
                "task_type": task_data.get("task_type"),
                "args": task_data.get("args"),
                "status": task_data.get("status"),
                "result": task_data.get("result"),
                "worker_id": task_data.get("worker_id"),
            })
    return tasks

