import os
import logging
from abc import ABC
from typing import List, Dict, Any
from firebase_admin import firestore


class Database(ABC):
    def __init__(self):
        pass

    def insert(self, data: Dict[str, Any]) -> None:
        pass

    def update(self, data: Dict[str, Any]) -> None:
        pass

    def delete(self, data: Dict[str, Any]) -> None:
        pass

    def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    def query_all(self) -> List[Dict[str, Any]]:
        pass

    def close(self) -> None:
        pass


class FireBaseDatabase(Database):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.db = firestore.client()
        self.collection = self.db.collection("user_jobs")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # set up logging to file
        # create firebasedb.log file in logs directory
        if os.path.exists("logs") == False:
            os.mkdir("logs")
        if os.path.exists("logs/firebasedb.log") == False:
            open("logs/firebasedb.log", "w").close()
        handler = logging.FileHandler("logs/firebasedb.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def insert(self, data: Dict[str, Any]) -> None:
        user_id = data.get("user_id")
        job_id = data.get("id")
        if user_id and job_id:
            user_doc = self.collection.document(user_id)
            # Create an array of jobs for the user
            user_doc.collection("jobs").document(job_id).set(data)
            self.logger.info(f"Inserted job {job_id} for user {user_id}")
        else:
            self.logger.error(
                f"Job {job_id} for user {user_id} does not exist")
            raise ValueError(f"Job {job_id} for user {user_id} does not exist")

    def update(self, data: Dict[str, Any]) -> None:
        user_id = data.get("user_id")
        job_id = data.get("id")

        if user_id and job_id:
            user_doc = self.collection.document(user_id)
            user_doc.collection("jobs").document(job_id).set(data)
            self.logger.info(f"Updated job {job_id} for user {user_id}")
        else:
            self.logger.error(
                f"Job {job_id} for user {user_id} does not exist")
            raise ValueError(f"Job {job_id} for user {user_id} does not exist")

    def delete(self, data: Dict[str, Any]) -> None:
        user_id = data.get("user_id")
        job_id = data.get("id")
        if user_id and job_id:
            user_doc = self.collection.document(user_id)
            user_doc.collection("jobs").document(job_id).delete()
            self.logger.info(f"Deleted job {job_id} for user {user_id}")
        else:
            self.logger.error(
                f"Job {job_id} for user {user_id} does not exist")
            raise ValueError(f"Job {job_id} for user {user_id} does not exist")

    def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        user_id = query.get("user_id")
        if user_id:
            user_doc = self.collection.document(user_id)
            results = user_doc.collection("jobs").stream()
            return [result.to_dict() for result in results]
        return []

    def query_all(self) -> List[Dict[str, Any]]:
        return super().query_all()

    def close(self) -> None:
        return super().close()
