from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(unique=True, pk=True)
    name = fields.CharField(max_length=32)
    phone_number = fields.CharField(max_length=16)
    address = fields.TextField()

    class Meta:
        table = 'users'

    def __str__(self):
        return f"[{self.id}] {self.name}"


class Promo(Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    file_id = fields.CharField(max_length=128)
    code = fields.CharField(max_length=16, unique=True)
    special_code = fields.CharField(max_length=6, unique=True)

    class Meta:
        table = 'promo'

    def __str__(self):
        return f"{self.user}: {self.special_code}"


class BlockedUser(Model):
    phone_number = fields.CharField(max_length=16)

    class Meta:
        table = 'blocked_user'

    def __str__(self):
        return self.phone_number
