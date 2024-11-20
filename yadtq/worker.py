import threading
import time
from kafka import KafkaConsumer
import redis
from yadtq.utils import (
    generate_uuid,
    send_heartbeat,
    validate_task,
    serialize_to_json,
    deserialize_from_json,
)

class Worker:
    def __init__(self, worker_id=None):
        # Assign a unique worker ID or generate one
        self.worker_id = generate_uuid()
        print(f"Initialized Worker with ID: {self.worker_id}")
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
        self.consumer = KafkaConsumer(
            "tasks",
            bootstrap_servers=["localhost:9092"],
            group_id="my-consumer-group",  # Shared group for multiple workers
            enable_auto_commit=True,
            session_timeout_ms=10000,
            heartbeat_interval_ms=3000,
            value_deserializer=lambda v: deserialize_from_json(v.decode("utf-8")),
        )
        print(f"Worker {self.worker_id} initialized.")

    def _process_task(self, task):
        """
        Process a single task by updating its status and performing the computation.
        """
        try:
            # Validate the task format
            validate_task(task)

            task_id = task["task_id"]
            task_type = task["task_type"]
            args = task["args"]

            # Update task status to 'processing'
            self.redis_client.hset(task_id, "status", "processing")
            self.redis_client.hset(task_id, "worker_id", self.worker_id)

            # Task execution logic
            if task_type == "add":
                result = sum(args)
            elif task_type == "subtract":
                result = args[0]-args[1]
            elif task_type == "multiply":
                result = args[0] * args[1]
            elif task_type == "divide":
                if args[1]==0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result=args[0]/args[1]
            else:
                raise ValueError(f"Unknown task type: {task_type}")

            # Simulate task processing delay
            time.sleep(5)

            # Update task status and result
            self.redis_client.hset(task_id, "status", "success")
            self.redis_client.hset(task_id, "result", result)
            print(f"Task {task_id} completed by worker {self.worker_id}: {result}")

        except Exception as e:
            # Handle task errors
            self.redis_client.hset(task_id, "status", "failed")
            self.redis_client.hset(task_id, "error", str(e))
            print(f"Task {task_id} failed by worker {self.worker_id}: {e}")

    def start(self):
        """
        Start the worker to process tasks from the Kafka queue.
        """
        # Start heartbeat thread
        heartbeat_thread = threading.Thread(
            target=send_heartbeat,
            args=(self.redis_client, self.worker_id),
            daemon=True,
        )
        heartbeat_thread.start()

        # Process tasks from the Kafka queue
        print(f"Worker {self.worker_id} listening for tasks...")
        for message in self.consumer:
            task = message.value
            threading.Thread(target=self._process_task, args=(task,)).start()

