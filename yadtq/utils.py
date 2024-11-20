import uuid
import json
import time
from datetime import datetime

# UUID Generation
def generate_uuid():
    return str(uuid.uuid4())

# Heartbeat Utility
def send_heartbeat(redis_client, worker_id, interval=5):
    while True:
        try:
            redis_client.hset(f"worker:{worker_id}", "status", "alive")
            redis_client.hset(f"worker:{worker_id}", "last_heartbeat", time.time())
            print(f"Heartbeat sent for worker {worker_id}")
        except Exception as e:
            print(f"Failed to send heartbeat for worker {worker_id}: {e}")
        time.sleep(interval)

# JSON Serialization/Deserialization
def serialize_to_json(data):
    try:
        return json.dumps(data)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Error serializing to JSON: {e}")

def deserialize_from_json(json_string):
    try:
        return json.loads(json_string)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Error deserializing from JSON: {e}")

# Timestamp Utility
def get_current_timestamp():
    return datetime.utcnow().isoformat()

# Task Validation
def validate_task(task):
    required_fields = ["task_id", "task_type", "args"]
    for field in required_fields:
        if field not in task:
            raise ValueError(f"Task is missing required field: {field}")
    if not isinstance(task["args"], list):
        raise ValueError("Task 'args' must be a list")

# Retry Logic
def retry(operation, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return operation()
        except Exception as e:
            if attempt < retries - 1:
                print(f"Retrying operation due to error: {e}")
                time.sleep(delay)
            else:
                raise

