#!/usr/bin/env python3
from yadtq.redis_backend import query_all_tasks
import json

tasks = query_all_tasks()
print(json.dumps(tasks, indent=4))

