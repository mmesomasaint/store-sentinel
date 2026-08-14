# app/schemas/store.py
from pydantic import BaseModel, HttpUrl, EmailStr, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class StoreCreate(BaseModel):
    name: str = Field(..., example="Luxury Apparel Store")
    url: HttpUrl = Field(..., example="https://myshopifystore.com")
    manager_email: EmailStr = Field(..., example="manager@myshopifystore.com")

class StoreResponse(BaseModel):
    id: str
    name: str
    url: str
    manager_email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BrokenLinkDetail(BaseModel):
    url: str
    status_code: int
    source_page: str

class AuditReportResponse(BaseModel):
    id: str
    store_id: str
    is_up: bool
    status_code: int
    response_time_ms: float
    total_links_scanned: int
    broken_links_found: int
    broken_links_details: List[BrokenLinkDetail]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
