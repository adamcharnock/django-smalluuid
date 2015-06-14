from django.core.exceptions import ValidationError
from django.db.models.fields import UUIDField
from django.utils import six
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
import smalluuid

from django_smalluuid import settings, forms


class SmallUUIDField(UUIDField):
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid short-form UUID."),
    }
    description = 'Short-form universally unique identifier'

    def __init__(self, verbose_name=None, uuid_class=settings.DEFAULT_CLASS, **kwargs):
        self.uuid_class = uuid_class
        if isinstance(self.uuid_class, six.string_types):
            self.uuid_class = import_string(uuid_class)
        super(SmallUUIDField, self).__init__(verbose_name, **kwargs)

    def get_db_prep_value(self, value, *args, **kwargs):
        if isinstance(value, six.string_types):
            value = self.uuid_class(value)
        return super(SmallUUIDField, self).get_db_prep_value(value, *args, **kwargs)

    def to_python(self, value):
        if value and not isinstance(value, self.uuid_class):
            try:
                return self.uuid_class(value)
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

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return None
        return self.uuid_class(int=value.int)


def uuid_default(version=None):
    def uuid_generator():
        return smalluuid.SmallUUID(version=version)
    return uuid_generator


def uuid_typed_default(version=None, type=None):
    def uuid_generator():
        return smalluuid.TypedSmallUUID(version=version, type=type)
    return uuid_generator
