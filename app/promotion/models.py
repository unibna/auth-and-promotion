from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    import app.user.models


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


class ValidConditionType(str, Enum):
    EVENT = "event"


class ValidConditionOperator(str, Enum):
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'


class ValidConditionValueType(str, Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"


class ValidConditionValueUnit(str, Enum):
    NUMBER = "number"
    PERCENT = "percent"
    STRING = "string"


class Condition(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, timezone="Asia/Ho_Chi_Minh")
    updated_at = fields.DatetimeField(auto_now=True, timezone="Asia/Ho_Chi_Minh")
    
    campaign: "fields.ForeignKeyRelation[Campaign]" = fields.ForeignKeyField('models.Campaign', related_name="campaign_conditions")
    type = fields.CharEnumField(ValidConditionType, max_length=32)
    operator = fields.CharEnumField(ValidConditionOperator, max_length=32,
                                    default=ValidConditionOperator.EQUAL)
    value_type = fields.CharEnumField(ValidConditionValueType, max_length=32)
    value = fields.CharField(max_length=256)
    value_unit = fields.CharEnumField(ValidConditionValueUnit, max_length=32)


class ValidResultType(str, Enum):
    VOUCHER = 'voucher'
    CASH = 'cash'


class ValidResultValueUnit(str, Enum):
    NUMBER = "number"
    PERCENT = "percent"
    STRING = "string"


class Result(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, timezone="Asia/Ho_Chi_Minh")
    updated_at = fields.DatetimeField(auto_now=True, timezone="Asia/Ho_Chi_Minh")
    campaign = fields.ForeignKeyField('models.Campaign', related_name="campaign_results")
    type = fields.CharEnumField(ValidResultType, max_length=32)
    value = fields.CharField(max_length=256)
    value_unit = fields.CharEnumField(ValidResultValueUnit, max_length=32)


class ValidVoucherType(str, Enum):
    DIRECT_DISCOUNT = 'direct_discount'
    GIFT = "gift"


class ValidVoucherValueUnit(str, Enum):
    NUMBER = "number"
    PERCENT = "percent"
    STRING = "string"


class Voucher(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, timezone="Asia/Ho_Chi_Minh")
    updated_at = fields.DatetimeField(auto_now=True, timezone="Asia/Ho_Chi_Minh")
    
    expired_at = fields.DatetimeField(timezone="Asia/Ho_Chi_Minh")
    claimed_at = fields.DatetimeField(auto_now_add=True, timezone="Asia/Ho_Chi_Minh")
    used_at = fields.DatetimeField(null=True, timezone="Asia/Ho_Chi_Minh")

    campaign = fields.ForeignKeyField('models.Campaign', related_name="campaign_vouchers")
    user_id = fields.BigIntField()
    type = fields.CharEnumField(ValidVoucherType, max_length=32)
    value = fields.CharField(max_length=256)
    value_unit = fields.CharEnumField(ValidVoucherValueUnit, max_length=32)
