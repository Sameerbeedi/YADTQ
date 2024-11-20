from kafka import KafkaProducer, KafkaConsumer
import json
from .config import KAFKA_CONFIG

def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer():
    return KafkaConsumer(
        KAFKA_CONFIG["topic"],
        bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
        group_id=KAFKA_CONFIG["group_id"],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=True,
    )

