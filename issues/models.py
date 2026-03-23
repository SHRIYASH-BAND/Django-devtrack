from abc import ABC, abstractmethod
from datetime import datetime

ISSUE_STATUS = ['open', 'in_progress', 'resolved', 'closed']
PRIORITY_STATUS = ['low', 'medium', 'high', 'critical']


class BaseEntity(ABC):

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key : value for key, value in self.__dict__.items()
        }
    
class Reporter(BaseEntity):

    def __init__(self, id: int, name: str, email: str, team: str):
        self.id = id
        self.name = name
        self.email = email
        self.team = team
    
    def validate(self):
        
        if not self.name:
            raise ValueError("Reporter name cannot be empty.")
        if '@' not in self.email:
            raise ValueError("Reporter email must be valid.")
        if '.com' not in self.email and '.in' not in self.email:
            raise ValueError("Email with only .com or .in domain is allowed.")
        if not self.team:
            raise ValueError("Reporter team cannot be empty.")


class Issue(BaseEntity):

    def __init__(self, id, title, description, status, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = str(datetime.now())

    def validate(self):
        
        if not self.title:
            raise ValueError("Issue title cannot be empty.")
        if self.status not in ISSUE_STATUS:
            raise ValueError("Invalid issue status provided.")
        if self.priority not in PRIORITY_STATUS:
            raise ValueError("Invalid issue priority provided.")

    def describe(self):
        return f"{self.title} [{self.priority}]"
    

class CriticalIssue(Issue):

    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"

class LowPriorityIssue(Issue):

    def describe(self):
        return f"{self.title} — low priority, handle when free"