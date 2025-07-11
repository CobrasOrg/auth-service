from uuid import uuid4
from typing import Dict, Optional

class InMemoryUserDB:
    def __init__(self):
        self.users_by_id: Dict[str, dict] = {}
        self.email_to_id: Dict[str, str] = {}

    def get_by_email(self, email: str) -> Optional[dict]:
        if not email:
            return None
        
        normalized_email = email.strip().lower()
        user_id = self.email_to_id.get(normalized_email)
        return self.users_by_id.get(user_id) if user_id else None
    
    def create(self, user_data: dict) -> dict:
        if not user_data or "email" not in user_data:
            raise ValueError("User data must contain email.")
        
        user_id = str(uuid4())
        email = user_data["email"].strip().lower()

        if email in self.email_to_id:
            raise ValueError("Email already exists.")

        user_data_copy = user_data.copy()
        user_data_copy["id"] = user_id
        
        self.users_by_id[user_id] = user_data_copy
        self.email_to_id[email] = user_id

        return user_data_copy

db = InMemoryUserDB()