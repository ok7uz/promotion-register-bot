from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(unique=True, pk=True)
    name = fields.CharField(max_length=32)
    phone_number = fields.CharField(max_length=16)
    address = fields.TextField()
    file_id = fields.CharField(max_length=128)
    promo_code = fields.CharField(max_length=16)
    special_code = fields.CharField(max_length=6)

    class Meta:
        table = 'users'

    def __str__(self):
        return f"[{self.id}] {self.name}"

