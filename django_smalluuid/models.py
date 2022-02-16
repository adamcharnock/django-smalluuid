import uuid

from django.core.exceptions import ValidationError
from django.db import connection
from django.db.models.fields import UUIDField
from django.utils.deconstruct import deconstructible
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
import smalluuid

from django_smalluuid import settings, forms


class SmallUUIDField(UUIDField):
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid short-form UUID."),
    }
    description = 'Short-form universally unique identifier'

    def __init__(self, verbose_name=None, uuid_class=settings.DEFAULT_CLASS, **kwargs):
        self.uuid_class = uuid_class
        if isinstance(self.uuid_class, str):
            self.uuid_class = import_string(uuid_class)
        # unique=True is a much more sensible default for UUIDs
        kwargs.setdefault('unique', True)
        super(SmallUUIDField, self).__init__(verbose_name, **kwargs)

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return value

        if isinstance(value, str):
            value = self.uuid_class(value)

        if hasattr(value, 'bytes'):
            # Make sure this is a non-small UUID so the db will know
            # how to handle it
            value = uuid.UUID(bytes=value.bytes)

        if connection.features.has_native_uuid_field:
            return value
        else:
            return value.hex

    def to_python(self, value):
        if value and not isinstance(value, self.uuid_class):
            try:
                if isinstance(value, str) and len(value) > 30:
                    return self.uuid_class(hex=value)
                else:
                    return self.uuid_class(small=value)
            except ValueError:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.ShortUUIDField,
            'uuid_class': self.uuid_class,
        }
        defaults.update(kwargs)
        return super(SmallUUIDField, self).formfield(**defaults)

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None
        return self.uuid_class(int=value.int)


@deconstructible
class UUIDDefault(object):

    def __init__(self, version=None):
        self.version = version

    def __call__(self):
        return smalluuid.SmallUUID(version=self.version)

uuid_default = UUIDDefault


@deconstructible
class UUIDTypedDefault(object):

    def __init__(self, version=None, type=None):
        self.version = version
        self.type = type

    def __call__(self):
        return smalluuid.TypedSmallUUID(version=self.version, type=self.type)

uuid_typed_default = UUIDTypedDefault
