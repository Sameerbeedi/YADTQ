# YADTQ<br>
Yet Another Distributed Task Queue<br>
## Overview<br>
- YADTQ is a simulation of a distributed task queue architecture. It enables clients to submit tasks (mathematical operations) which are processed by distributed workers. 
- The system provides real-time updates on the status of tasks through a simple graphical user interface (GUI).
## Features
###  Distributed Task Processing:
- Tasks are distributed among multiple workers.
- Workers handle mathematical operations submitted by clients.
- Real-time Status Monitoring:
-  Track task statuses through the GUI or terminal commands.
###  Scalable Worker Management:
- Start multiple workers with ease. Each worker runs in a separate terminal.
### Technology Stack:
- Redis: Backend data storage.
- Kafka: Message broker for communication between clients and workers.
## Project Structure
### Examples Directory
- Producer Code: Contains the logic for client input and task submission.
- Worker Code: Implements worker initialization and operation handling.
- Query Tasks: Displays the status of all tasks.
### YADTQ Directory
- The core module implementing the distributed task queue architecture.<br>
#### Handles:
- Task submission.
- Worker heartbeat signals.
- Communication via Redis and Kafka.
### Main Directory
#### Includes:
- Requirements and setup files for installing dependencies.
- gui.py: A graphical user interface for interacting with the system.
### How to Run the Project
#### Install Dependencies:
1. Ensure all requirements are installed:
`pip install -r requirements.txt`<br>
`pip install -e . `<br>
2. Run the GUI:
Start the application:<br>
`python gui.py`<br>
*(Use python3 gui.py if required by your environment.)*
### Interact with the System:
1. Start Workers:
- Click the "Start Workers" button in the GUI to start as many workers as you need. Each worker opens in a separate terminal.
2. Submit Tasks:
- Click the "Submit Task" button.
- Enter the number of tasks and specify the operations (e.g., addition, subtraction) along with the operands.
- A terminal will open to allow input for task details.
3. View Task Queue:
- Click the "Task Queue" button to view the status of all tasks.
## Technologies Used
- Backend: Redis for data storage.
- Broker: Kafka for task messaging.
- GUI: Python-based graphical interface.
## Future Enhancements
- Add support for more complex operations.
- Broadcasting : Implement a broadcasting mechanism to efficiently distribute task updates to all connected clients and workers in real-time.
- Monitoring and Reporting : Develop a comprehensive monitoring service
- Logging
- Expand monitoring features in the GUI.
