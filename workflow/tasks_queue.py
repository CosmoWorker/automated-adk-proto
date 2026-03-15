from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class TaskState(str, Enum):
    new = "new"
    processing = "processing"
    completed = "completed"

@dataclass
class Task:
    id: int
    issue_txt: str
    state: TaskState= TaskState.new

class TaskQueue:
    def __init__(self):
        self.tasks: List[Task] = []
        self.counter = 0
    
    def add_task(self, issue_text: str) -> Task:
        self.counter +=1 
        task = Task(id=self.counter, issue_txt=issue_text)
        self.tasks.append(task)
        return task
    
    def next_task(self) -> Optional[Task]:
        for task in self.tasks:
            if task.state == TaskState.new:
                task.state =  TaskState.processing
                return task
        return None

    def mark_completed(self, task: Task):
        task.state = TaskState.completed