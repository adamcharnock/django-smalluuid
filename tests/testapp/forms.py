from django import forms
from smalluuid.smalluuid import TypedSmallUUID
from django_smalluuid.forms import ShortUUIDField


class TestForm(forms.Form):
    uuid = ShortUUIDField()


class TypedTestForm(forms.Form):
    uuid = ShortUUIDField(uuid_class=TypedSmallUUID)
