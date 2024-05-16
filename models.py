from typing import Optional
from pydantic import BaseModel

class ItemPayload(BaseModel):
    Aggregator: str
    BankName: str
    Reason: str