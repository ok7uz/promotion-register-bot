from tortoise.models import Model
from tortoise import fields


class User(Model):
    """
    User model representing a user in the system.
    """
    id = fields.IntField(pk=True, unique=True)
    name = fields.CharField(max_length=32)
    phone_number = fields.CharField(max_length=16, unique=True)
    address = fields.TextField()

    class Meta:
        table = 'users'
        indexes = ["phone_number"]

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"


class Code(Model):
    """
    Code model representing a code.
    """
    code = fields.CharField(max_length=16, pk=True, unique=True)

    class Meta:
        table = 'codes'
        indexes = ["code"]

    def __str__(self) -> str:
        return self.code


class Promo(Model):
    """
    Promo model representing a promotional code associated with a user.
    """
    user = fields.ForeignKeyField('models.User', related_name='promos', on_delete=fields.CASCADE)
    file_id = fields.CharField(max_length=128)
    code = fields.OneToOneField('models.Code', related_name='promo', on_delete=fields.CASCADE)
    special_code = fields.CharField(max_length=6, unique=True)

    class Meta:
        table = 'promo'
        indexes = ["code", "special_code"]

    def __str__(self) -> str:
        return f"{self.user}: {self.special_code}"


class BlockedUser(Model):
    """
    BlockedUser model representing a user that has been blocked.
    """
    phone_number = fields.CharField(max_length=16, unique=True)

    class Meta:
        table = 'blocked_user'
        indexes = ["phone_number"] 

    def __str__(self) -> str:
        return self.phone_number
