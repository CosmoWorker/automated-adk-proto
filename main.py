import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from workflow.tasks_queue import TaskQueue
from samp_agent.agent import root_agent

queue = TaskQueue()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def main():
    print("Hello from adk-samp!")


async def worker():
    while True:    
        task = queue.next_task()
        if task:
            result = root_agent.run_async(task.issue_txt)
            await asyncio.sleep(2)
            queue.mark_completed(task)
        else:
            await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_task = asyncio.create_task(worker())
    yield

    worker_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.post("/task")
def create_task(issue_txt: str):
    task = queue.add_task(issue_txt)
    return {"message": "Task queued", "task_id": task.id}

if __name__ == "__main__":
    main()
