from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[UserRole] = UserRole.user

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Optional[UserRole] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedTasks(BaseModel):
    tasks: List[TaskOut]
    total: int

class AuthResponse(BaseModel):
    success: bool
    data: dict
    message: str
