
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Auth
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Animals & Care
class CareRecordBase(BaseModel):
    date: date
    description: str
    done: bool = False
class CareRecordCreate(CareRecordBase): pass
class CareRecord(CareRecordBase):
    id: int
    class Config: from_attributes = True

class AnimalBase(BaseModel):
    name: str
    species: str
    arrival_date: date
    status: Optional[str] = "actif"
    notes: Optional[str] = None
class AnimalCreate(AnimalBase): pass
class Animal(AnimalBase):
    id: int
    care_records: List[CareRecord] = []
    class Config: from_attributes = True

# Tasks
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_at: Optional[datetime] = None
    animal_id: Optional[int] = None
    assigned_to_user_id: Optional[int] = None
class TaskCreate(TaskBase):
    send_sms: bool = False
    send_whatsapp: bool = False
class Task(TaskBase):
    id: int
    is_done: bool
    created_at: datetime
    class Config: from_attributes = True

# Stocks
class StockItemBase(BaseModel):
    name: str
    quantity: int = 0
    threshold: int = 0
class StockItemCreate(StockItemBase): pass
class StockItemUpdate(BaseModel):
    quantity: Optional[int] = None
    threshold: Optional[int] = None
class StockItem(StockItemBase):
    id: int
    class Config: from_attributes = True
