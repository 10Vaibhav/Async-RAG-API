from rq import SimpleWorker
from client.rq_client import queue
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    worker = SimpleWorker([queue], connection=queue.connection)
    worker.work()
