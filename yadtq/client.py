from .kafka_utils import create_producer
from .redis_backend import redis_client
from kafka import KafkaProducer
from yadtq.utils import generate_uuid ,serialize_to_json
import uuid
import json
import redis



def get_kafka_producer():
    """Initialize and return a Kafka producer instance."""
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

# Initialize Redis for storing task status/results
result_backend = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def query_task_status(task_id):
    """
    Query the status of a task using its task_id from Redis.
    """
    task_data = result_backend.hgetall(task_id)
    if not task_data:
        return None
    
    task_info = {
        "task_id": task_id,
        "task_type": task_data.get("task_type", ""),
        "args": task_data.get("args", ""),
        "status": task_data.get("status", ""),
        "result": task_data.get("result", ""),
        "worker": task_data.get("worker_id", ""),
    }
    return task_info
'''   
def submit_task(task_type, args):
    task_id = str(uuid.uuid4())
    task = {"task_id": task_id, "task_type": task_type, "args": args}
    redis_client.hset(task_id, "status", "queued")
    redis_client.hset(task_id, "task_type", task_type)
    redis_client.hset(task_id, "args", json.dumps(args))
    producer = create_producer()
    producer.send("tasks", task)
    producer.close()
    return task_id
'''
def submit_task(task_type, args):
    task_id = generate_uuid()  # Generate unique task ID
    task = {
        "task_id": task_id,
        "task_type": task_type,
        "args": args,
    }

    # Store initial task status in Redis
    redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
    redis_client.hset(task_id, "status", "queued")
    redis_client.hset(task_id, "task_type", task_type)
    redis_client.hset(task_id, "args", serialize_to_json(args))  # Store args in JSON format

    try:
        producer=get_kafka_producer()
        # Send task to Kafka queue
        future = producer.send("tasks", task)
        future.get(timeout=10)  # Wait for message to be sent
        print(f"Task {task_id} successfully sent to Kafka.")
    except Exception as e:
        print(f"Error sending task {task_id} to Kafka: {e}")
    
    return task_id


