from django.test import TestCase
from django.core.exceptions import ValidationError
from formative.models import FormativeBlob, InlineFormativeBlob
from tests.testproject.testapp.models import Book


class TestFormativeTypeValidation(TestCase):
    def test_invalid_type(self):
        with self.assertRaises(ValidationError) as e:
            FormativeBlob(unique_identifier='invalid',
                          formative_type='invalid',
                          json_data='{}')
        self.assertEqual(e.exception.messages, ['Invalid type: invalid.'])

    def test_valid_type(self):
        blob = FormativeBlob(unique_identifier='valid',
                             formative_type='simple',
                             json_data='{}')
        try:
            blob.full_clean()
        except ValidationError as e:
            self.fail('ValidationError raised: %s' % e)


class TestFormativeBlob(TestCase):
    def setUp(self):
        self.blob = FormativeBlob(unique_identifier='identifier',
                                  formative_type='simple',
                                  json_data='{}')
        self.blob.save()

    def test_str(self):
        self.assertEqual(str(self.blob), 'identifier (Simple)')


class TestInlineFormativeBlob(TestCase):
    def setUp(self):
        book = Book(title='Gunmachine')
        book.save()
        self.blob = InlineFormativeBlob(
            content_object=book,
            sortorder=0,
            formative_type='simple',
            json_data='{}')

    def test_str(self):
        self.assertEqual(str(self.blob), 'Simple')
