from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from app.user.models import User


class ValidCampaignStatus(str, Enum):
    DRAFT = "draft"
    WAITING = "waiting"
    RUNNING = "running"
    PAUSE = "pause"
    COMPLETED = "completed"
    DELETED = "deleted"


class ValidCampaignType(str, Enum):
    DIRECT_APPLY = "direct_apply"
    ISSUE_VOUCHER = "issue_voucher"


class ValidDataSource(str, Enum):
    EVENT = "event"
    SEGMENT = "segment"


class Campaign(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, timezone="Asia/Ho_Chi_Minh")
    updated_at = fields.DatetimeField(auto_now=True, timezone="Asia/Ho_Chi_Minh")
    deleted_at = fields.DatetimeField(null=True, timezone="Asia/Ho_Chi_Minh")

    start_at = fields.DatetimeField(timezone="Asia/Ho_Chi_Minh")
    end_at = fields.DatetimeField(timezone="Asia/Ho_Chi_Minh")
    
    name = fields.CharField(max_length=128)
    status = fields.CharEnumField(ValidCampaignStatus, 
                                default=ValidCampaignStatus.DRAFT,
                                max_length=16)
    type = fields.CharEnumField(ValidCampaignType, max_length=32)
    total_vouchers = fields.IntField(default=0)

    async def validate_start_at(self, value):
        if value < datetime.now():
            raise ValueError("start_at can not be smaller than the current time")

    async def validate_end_at(self, value):
        if not value:
            return
        if value < datetime.now():
            raise ValueError("end_at can not be smaller than the current time")
        if self.start_at >= value:
            raise ValueError("end_at can not be smaller than start_at")
        
    async def validate_total_vouchers(self, value):
        if value < 0:
            raise ValueError("total_voucher must be greater than 0")


class Condition(Model):
    pass
