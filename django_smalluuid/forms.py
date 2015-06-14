from django.core.exceptions import ValidationError
from django.forms import UUIDField
from django.utils import six
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from django_smalluuid import settings


class ShortUUIDField(UUIDField):
    default_error_messages = {
        'invalid': _('Enter a valid short-form UUID.'),
    }

    def __init__(self, uuid_class=settings.DEFAULT_CLASS, *args, **kwargs):
        self.uuid_class = uuid_class
        if isinstance(self.uuid_class, six.string_types):
            self.uuid_class = import_string(uuid_class)
        super(ShortUUIDField, self).__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, self.uuid_class):
            return six.text_type(value)
        return value

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if not isinstance(value, self.uuid_class):
            try:
                value = self.uuid_class(value)
            except ValueError:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value
