from django.db import models
from django_smalluuid.models import SmallUUIDField, uuid_default, uuid_typed_default


class TestModel(models.Model):
    uuid = SmallUUIDField(default=uuid_default())


class TypedTestModel(models.Model):
    uuid = SmallUUIDField(default=uuid_typed_default(type=42))
