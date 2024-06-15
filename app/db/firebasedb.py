from abc import ABC
from collections import defaultdict
import os
from typing import List, Dict, Any

from app.models.job import JobStatus
from firebase_admin import firestore

import logging



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
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    def insert(self, data: Dict[str, Any]) -> None:
        user_id = data.get("user_id")
        job_id = data.get("job_id")
        if user_id and job_id:
            user_doc = self.collection.document(user_id)
            # Create an array of jobs for the user
            user_doc.collection("jobs").document(job_id).set(data)
            self.logger.info(f"Inserted job {job_id} for user {user_id}")
        else:
            self.logger.error(f"Job {job_id} for user {user_id} does not exist")
            raise ValueError(f"Job {job_id} for user {user_id} does not exist")

    def update(self, data: Dict[str, Any]) -> None:
        user_id = data.get("user_id")
        job_id = data.get("job_id")
        
        if user_id and job_id:
            user_doc = self.collection.document(user_id)
            user_doc.collection("jobs").document(job_id).set(data)
            self.logger.info(f"Updated job {job_id} for user {user_id}")
        else:
            self.logger.error(f"Job {job_id} for user {user_id} does not exist")
            raise ValueError(f"Job {job_id} for user {user_id} does not exist")        


    def delete(self, data: Dict[str, Any]) -> None:
        user_id = data.get("user_id")
        job_id = data.get("job_id")
        if user_id and job_id:
            user_doc = self.collection.document(user_id)
            user_doc.collection("jobs").document(job_id).delete()
            self.logger.info(f"Deleted job {job_id} for user {user_id}")
        else:
            self.logger.error(f"Job {job_id} for user {user_id} does not exist")
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







# Copilot ignore:
    # def update(self, data: Dict[str, Any]) -> None:
    #     # Remove job from one status and add to another
    #     # Find the job with the job_id in firestore and find its status
    #     # Delete the job from the current status and add it to the new status
    #     user_id = data.get("user_id")
    #     status = data.get("status")
    #     job_id = data.get("job_id")
    #     from_status = data.get("from_status")
    #     if user_id and status and job_id:
    #         user_doc = self.collection.document(user_id)
    #         status_collection = user_doc.collection(status)
    #         status_collection.document(job_id).set(data)
    #         status_collection = user_doc.collection(from_status)
    #         status_collection.document(job_id).delete()
    #     self.logger.info(f"Updated job {job_id} for user {user_id} from {from_status} to {status}")

    # def delete(self, data: Dict[str, Any]) -> None:
    #     user_id = data.get("user_id")
    #     status = data.get("status")
    #     job_id = data.get("job_id")
    #     if user_id and status and job_id:
    #         user_doc = self.collection.document(user_id)
    #         status_collection = user_doc.collection(status)
    #         status_collection.document(job_id).delete()
    #     self.logger.info(f"Deleted job {job_id} for user {user_id} in status {status}")

    # def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
    #     # Query by user_id and get entire job board
    #     user_id = query.get("user_id")
    #     self.logger.info(f"Queried jobs for user {user_id}")
    #     if user_id:
    #         user_doc = self.collection.document(user_id)
    #         results = defaultdict(list)
    #         for status in JobStatus:
    #             status_collection = user_doc.collection(status.value)
    #             status_results = status_collection.stream()
    #             for result in status_results:
    #                 results[status.value].append(result.to_dict())
    #         return results
    #     return []

    
    # def query_all(self) -> List[Dict[str, Any]]:
    #     pass

    # def close(self) -> None:    
    #     pass        



# if __name__ == "__main__":
#     import firebase_admin
#     import firebase_admin.auth

#     creds = firebase_admin.credentials.Certificate("/workspaces/job-hunter/serviceAccountCreds.json")

#     default_app = firebase_admin.initialize_app(creds)

#     db = FireBaseDatabase()    
#     job_board = JobBoard(
#         user_id="123456",
#         job_id="123456",
#         status=JobStatus.wishlist,
#         company_name="Google",
#         position="Software Engineer",
#         salary="$120,000",
#         location="Mountain View, CA",
#         job_url="https://careers.google.com/jobs/results/123456"
#     )

#     # Test insert
#     db.insert(job_board.model_dump())

#     results = db.query({"user_id": "123456"})
#     print("After insert\n", results)
#     # Test update
#     from_job = job_board.status
#     job_board.status = JobStatus.applied

#     db.update(job_board.model_dump(), from_job)

#     # Test query
#     results = db.query({"user_id": "123456"})
#     print(results)

#     # Test delete
#     # db.delete(job_board.model_dump())

#     db.close()






# Copilot ignore:
# class FireBaseDatabase(Database):
#     def __init__(self):
#         self.db = firestore.client()
#         self.collection = self.db.collection("jobs")

#     def insert(self, data: Dict[str, Any]) -> None:
#         self.collection.document().set(data)

#     def update(self, data: Dict[str, Any]) -> None:
#         job_id = data.get("job_id")
#         if job_id:
#             self.collection.document(job_id).set(data)

#     def delete(self, data: Dict[str, Any]) -> None:
#         job_id = data.get("job_id")
#         if job_id:
#             self.collection.document(job_id).delete()

#     def query(self, field: str, value: str) -> List[Dict[str, Any]]:
#         results = self.collection.where(field_path=field, value=value, op_string="==").stream()
#         return [result.to_dict() for result in results]
    
#     def query_all(self) -> List[Dict[str, Any]]:
#         results = self.collection.stream()
#         return [result.to_dict() for result in results]
    
#     def close(self) -> None:
#         pass


# # Test the FireBaseDatabase class by creating an instance and inserting a job board entry.


# if __name__ == "__main__":
#     import firebase_admin
#     import firebase_admin.auth

#     creds = firebase_admin.credentials.Certificate("/workspaces/job-hunter/serviceAccountCreds.json")

#     default_app = firebase_admin.initialize_app(creds)

#     db = FireBaseDatabase()
#     job_board = JobBoard(
#         job_id="123456",
#         status=JobStatus.wishlist,
#         company_name="Google",
#         position="Software Engineer",
#         salary="$120,000",
#         location="Mountain View, CA",
#         job_url="https://careers.google.com/jobs/results/123456"
#     )
    
#     # Test insert
#     db.insert(job_board.model_dump())

#     # Test update
#     job_board.status = JobStatus.applied
#     db.update(job_board.model_dump())

#     # Test query
#     results = db.query("status", JobStatus.applied)
#     print(results)

#     # Test query all
#     results = db.query_all()
#     print(results)

#     # Test delete
#     db.delete(job_board.model_dump())

#     # Test query all after delete
#     results = db.query_all()
#     print(results)

#     db.close()

