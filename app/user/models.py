from tortoise import fields
from tortoise.models import Model

from app.common.security.crypter import crypter


class User(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    username = fields.CharField(max_length=32, unique=True)
    email = fields.CharField(max_length=128, unique=True, null=True)
    phone = fields.CharField(max_length=12, unique=True, null=True)
    password = fields.CharField(max_length=256)
    full_name = fields.CharField(max_length=128, unique=True, null=True)
    birthday = fields.DateField(null=True)
    last_login = fields.DatetimeField(null=True)

    async def password_validator(self):
        if self.password and not crypter.is_hashed(self.password):
            self.password = crypter.hash_password(self.password.encode())
        
    async def save(self, *args, **kwargs):
        await self.password_validator()
        await super().save(*args, **kwargs)
