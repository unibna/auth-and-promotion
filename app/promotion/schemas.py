from datetime import (
    datetime,
)
from pydantic import (
    BaseModel,
)
from typing import (
    List,
    Optional,
)


class CampaignCreate(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    name: str = None
    type: str = None
    total_vouchers: int = None


class CampaignUpdate(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    name: str = None
    status: str = None
    type: str = None
    total_vouchers: int = None


class CampaignResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    name: str = None
    status: str = None
    type: str = None
    total_vouchers: int = None


class ConditionCreate(BaseModel):
    type: str
    operator: str
    value_type: str
    value: str
    value_unit: str


class ConditionResponse(BaseModel):
    campaign_id: int
    type: str
    operator: str
    value_type: str
    value: str
    value_unit: str


class ResultCreate(BaseModel):
    type: str
    value: str
    value_unit: str


class ResultResponse(BaseModel):
    campaign_id: int
    type: str
    value: str
    value_unit: str
