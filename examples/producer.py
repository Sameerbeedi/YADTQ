'''
#!/usr/bin/env python3
import argparse
from yadtq.client import submit_task

# Set up argument parser
parser = argparse.ArgumentParser(description="Submit a task to the YADTQ system.")
parser.add_argument("task_type", type=str, help="Type of task (e.g., 'add', 'multiply', 'divide', 'subtract')")
parser.add_argument("args", nargs="+", type=float, help="Arguments for the task (e.g., numbers to process)")

# Parse command-line arguments
args = parser.parse_args()
task_type = args.task_type
task_args = args.args

# Submit the task
task_id = submit_task(task_type, task_args)
print(f"Task submitted successfully! Task ID: {task_id}")
'''
'''
#this sends tasks separately
#!/usr/bin/env python3
import argparse
from yadtq.client import submit_task

# Set up argument parser
parser = argparse.ArgumentParser(description="Submit multiple tasks to the YADTQ system.")
parser.add_argument(
    "num_tasks",
    type=int,
    help="Number of tasks to submit.",
)

# Parse command-line arguments
args = parser.parse_args()
num_tasks = args.num_tasks

# Loop to collect tasks from the user
for i in range(num_tasks):
    print(f"\nEntering details for task {i + 1}:")

    # Get the task type
    task_type = input("Enter task type (e.g., 'add', 'multiply', 'divide', 'subtract'): ").strip()

    # Get the task arguments
    while True:
        try:
            task_args = input("Enter arguments as space-separated numbers (e.g., '4 5 6'): ").strip()
            task_args = [float(x) for x in task_args.split()]
            break
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

    # Submit the task
    task_id = submit_task(task_type, task_args)
    print(f"Task {i + 1} submitted successfully! Task ID: {task_id}")
'''

#this sends all the tasks at once to check whether workers are working properly
#!/usr/bin/env python3
import argparse
import threading
from yadtq.client import submit_task

def collect_tasks(num_tasks):
    """
    Collect tasks from the user.

    :param num_tasks: Number of tasks to collect.
    :return: List of tasks with their types and arguments.
    """
    tasks = []
    for i in range(num_tasks):
        print(f"\nEntering details for task {i + 1}:")

        # Get the task type
        task_type = input("Enter task type (e.g., 'add', 'multiply', 'divide', 'subtract'): ").strip()

        # Get the task arguments
        while True:
            try:
                task_args = input("Enter arguments as space-separated numbers (e.g., '4 5 6'): ").strip()
                task_args = [float(x) for x in task_args.split()]
                break
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")

        tasks.append((task_type, task_args))
    return tasks

def submit_task_thread(task_type, task_args):
    """
    Submit a task in a separate thread.

    :param task_type: Task type (e.g., 'add', 'multiply').
    :param task_args: Arguments for the task.
    """
    task_id = submit_task(task_type, task_args)
    print(f"Task submitted successfully! Task ID: {task_id}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Submit multiple tasks to the YADTQ system.")
    parser.add_argument(
        "num_tasks",
        type=int,
        help="Number of tasks to submit.",
    )

    # Parse command-line arguments
    args = parser.parse_args()
    num_tasks = args.num_tasks

    # Collect tasks from the user
    tasks = collect_tasks(num_tasks)

    # Submit all tasks concurrently
    threads = []
    for task_type, task_args in tasks:
        thread = threading.Thread(target=submit_task_thread, args=(task_type, task_args))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\nAll tasks have been submitted successfully!")

