import tkinter as tk
from tkinter import messagebox, simpledialog
from threading import Thread
import subprocess
import os
import sys

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Queue Management")
        self.create_widgets()

    def create_widgets(self):
        self.create_worker_button = tk.Button(self.root, text="Create Worker", command=self.create_worker)
        self.create_worker_button.grid(row=0, column=0, padx=10, pady=10)

        self.submit_task_button = tk.Button(self.root, text="Submit Tasks", command=self.submit_tasks)
        self.submit_task_button.grid(row=1, column=0, padx=10, pady=10)

        self.query_tasks_button = tk.Button(self.root, text="View All Task Status", command=self.query_all_tasks)
        self.query_tasks_button.grid(row=2, column=0, padx=10, pady=10)

        self.output_box = tk.Text(self.root, height=15, width=60)
        self.output_box.grid(row=3, column=0, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.root, command=self.output_box.yview)
        self.scrollbar.grid(row=3, column=1, sticky="ns", pady=10)
        self.output_box.config(yscrollcommand=self.scrollbar.set)

    def create_worker(self):
        """
        Start a worker in a new terminal window.
        """
        def worker_thread():
            try:
                # Open a new terminal to run the worker
                subprocess.Popen(
                    ["gnome-terminal", "--", sys.executable, os.path.join("examples", "worker.py")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.output_box.insert(tk.END, "Worker started in a new terminal.\n")
            except Exception as e:
                self.output_box.insert(tk.END, f"Error creating worker: {e}\n")

        Thread(target=worker_thread).start()

    def submit_tasks(self):
        """
        Submit tasks to the queue using the producer.py script.
        """
        try:
            num_tasks = simpledialog.askinteger("Input", "Enter the number of tasks to submit:")
            if num_tasks is not None and num_tasks > 0:
                # Run producer.py interactively
                subprocess.run(
                    ["gnome-terminal", "--", sys.executable, os.path.join("examples", "producer.py"), str(num_tasks)],
                    check=True
                )
                self.output_box.insert(tk.END, f"{num_tasks} tasks submitted interactively in a terminal.\n")
            else:
                messagebox.showerror("Error", "Number of tasks must be a positive integer.")
        except Exception as e:
            self.output_box.insert(tk.END, f"Error submitting tasks: {e}\n")

    def query_all_tasks(self):
        """
        Query the status of all tasks from the task queue.
        """
        def query_thread():
            try:
                # Run query_tasks.py to retrieve all task statuses
                result = subprocess.run(
                    [sys.executable, os.path.join("examples", "query_tasks.py")],
                    capture_output=True,
                    text=True,
                    check=True
                )
                tasks = result.stdout
                self.output_box.insert(tk.END, f"All Task Statuses:\n{tasks}\n")
            except subprocess.CalledProcessError as e:
                self.output_box.insert(tk.END, f"Error querying tasks: {e}\n")
            except Exception as e:
                self.output_box.insert(tk.END, f"Unexpected error: {e}\n")

        Thread(target=query_thread).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
