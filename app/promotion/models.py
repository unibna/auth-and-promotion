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


class Campaign(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    start_at = fields.DatetimeField()
    end_at = fields.DatetimeField()
    
    name = fields.CharField(max_length=128)
    status = fields.CharEnumField(ValidCampaignStatus, 
                                default=ValidCampaignStatus.DRAFT,
                                max_length=16)
    type = fields.CharEnumField(ValidCampaignType, max_length=32)
    total_vouchers = fields.IntField(default=0)


class Condition(Model):
    pass
