from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=False)
    username = fields.CharField(max_length=32, unique=True)
    email = fields.CharField(max_length=128, unique=True, null=True)
    phone = fields.CharField(max_length=12, unique=True, null=True)
    password = fields.CharField(max_length=256)
    full_name = fields.CharField(max_length=128, unique=True, null=True)
    birthday = fields.DateField(null=True)
    last_login = fields.DatetimeField(null=True)
