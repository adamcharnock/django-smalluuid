from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import connection
from smalluuid import SmallUUID
from smalluuid import TypedSmallUUID

from django_smalluuid import models, forms
from django_smalluuid.forms import ShortUUIDField
from testapp.forms import TestForm, TypedTestForm
from testapp.models import TestModel, TypedTestModel


class ModelFieldTestCase(TestCase):

    def test_unique_by_default(self):
        field = models.SmallUUIDField()
        self.assertTrue(field.unique)

    def test_force_not_unique(self):
        field = models.SmallUUIDField(unique=False)
        self.assertFalse(field.unique)

    def test_to_python(self):
        field = models.SmallUUIDField()
        out = field.to_python('IBNApQOzTHGzdjkSt6t-Jg')
        self.assertIsInstance(out, SmallUUID)

    def test_to_python_invalid_value(self):
        field = models.SmallUUIDField()
        self.assertRaises(ValidationError, field.to_python, 'xxx')

    def test_to_python_custom_class(self):
        field = models.SmallUUIDField(uuid_class=TypedSmallUUID)
        out = field.to_python('IBNApQOzTHGzdjkSt6t-Jg')
        self.assertIsInstance(out, TypedSmallUUID)

    def test_to_python_class_string(self):
        field = models.SmallUUIDField(uuid_class='smalluuid.TypedSmallUUID')
        out = field.to_python('IBNApQOzTHGzdjkSt6t-Jg')
        self.assertIsInstance(out, TypedSmallUUID)

    def test_prep(self):
        field = models.SmallUUIDField()
        out = field.get_db_prep_value(SmallUUID('IBNApQOzTHGzdjkSt6t-Jg'), connection=connection)
        self.assertEqual(out, '201340a503b34c71b3763912b7ab7e26')

    def test_prep_none(self):
        field = models.SmallUUIDField()
        out = field.get_db_prep_value(None, connection=connection)
        self.assertEqual(out, None)

    def test_form_field(self):
        field = models.SmallUUIDField()
        self.assertIsInstance(field.formfield(), forms.ShortUUIDField)


class FormFieldTestCase(TestCase):

    def test_valid(self):
        form = TestForm({'uuid': 'IBNApQOzTHGzdjkSt6t-Jg'})
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid(self):
        form = TestForm({'uuid': 'xxx'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_none(self):
        form = TestForm({'uuid': None})
        self.assertFalse(form.is_valid(), form.errors)

    def test_typed_valid(self):
        form = TypedTestForm({'uuid': 'IBNApQOzTHGzdjkSt6t-Jg'})
        self.assertTrue(form.is_valid(), form.errors)

    def test_typed_invalid(self):
        form = TypedTestForm({'uuid': 'xxx'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_typed_none(self):
        form = TypedTestForm({'uuid': None})
        self.assertFalse(form.is_valid(), form.errors)

    def test_prepare_value(self):
        field = ShortUUIDField()
        self.assertEqual(field.prepare_value('IBNApQOzTHGzdjkSt6t-Jg'), 'IBNApQOzTHGzdjkSt6t-Jg')


class ModelTestCase(TestCase):

    def test_value_created(self):
        model = TestModel.objects.create()
        self.assertIsInstance(model.uuid, SmallUUID)
        self.assertEqual(model.uuid.version, 4)
        self.assertEqual(len(str(model.uuid)), 22)

    def test_persist_reload(self):
        model = TestModel.objects.create()
        model.save()
        uuid = TestModel.objects.values_list('uuid', flat=True)[0]
        self.assertEqual(model.uuid, uuid)

    def test_filter(self):
        TestModel.objects.create()
        model = TestModel.objects.create()
        TestModel.objects.create()

        uuid = TestModel.objects.filter(uuid=str(model.uuid)).values_list('uuid', flat=True)[0]
        self.assertIsInstance(model.uuid, SmallUUID)
        self.assertEqual(model.uuid, uuid)


class TypedModelTestCase(TestCase):

    def test_value_created(self):
        model =TypedTestModel.objects.create()
        self.assertIsInstance(model.uuid, TypedSmallUUID)
        self.assertEqual(model.uuid.version, 4)
        self.assertEqual(model.uuid.type, 42)
        self.assertEqual(len(str(model.uuid)), 22)

    def test_persist_reload(self):
        model = TypedTestModel.objects.create()
        model.save()
        uuid = TypedTestModel.objects.values_list('uuid', flat=True)[0]
        self.assertEqual(model.uuid, uuid)

