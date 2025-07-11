from uuid import uuid4
from typing import Dict, List, Optional
from datetime import datetime, timezone

class InMemoryUserDB:
    def __init__(self):
        self.users_by_id: Dict[str, dict] = {}
        self.email_to_id: Dict[str, str] = {}

    def reset(self):
        self.users_by_id.clear()
        self.email_to_id.clear()

    def get_by_id(self, user_id: str) -> Optional[dict]:
        if not user_id:
            return None
        return self.users_by_id.get(user_id)

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

    def get_all(self) -> List[dict]:
        return list(self.users_by_id.values())
    
    def update(self, user_id: str, updates: dict) -> Optional[dict]:
        if not user_id or not updates:
            return None
            
        user = self.get_by_id(user_id)
        if not user:
            return None

        if "email" in updates:
            old_email = user["email"].strip().lower()
            new_email = updates["email"].strip().lower()

            if new_email != old_email:
                if new_email in self.email_to_id:
                    raise ValueError("Email already exists.")
                
                del self.email_to_id[old_email]
                self.email_to_id[new_email] = user_id

        user.update(updates)
        user["updatedAt"] = datetime.now(timezone.utc)
        return user

    def delete(self, user_id: str) -> Optional[dict]:
        if not user_id:
            return None
            
        user = self.users_by_id.pop(user_id, None)
        if user and "email" in user:
            email = user["email"].strip().lower()
            self.email_to_id.pop(email, None)
        return user
    
db = InMemoryUserDB()