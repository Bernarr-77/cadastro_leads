from pydantic import BaseModel, EmailStr,Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime

class LeadInput(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumber

class LeadsProcess(LeadInput):
    id: int | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "novo"

