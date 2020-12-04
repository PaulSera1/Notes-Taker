from django.test import TestCase
from .models import Note
from django.contrib.auth.models import User

class NoteTest(TestCase):
    # create Note object
    def setUp(self):
        Note.objects.create(
            title='Note Title',
            body='this is the note body',
            author=User.objects.create_user('john_smith')
        )
    # test note author foreignkey and title
    def test_note_title(self):
        note = Note.objects.get(title='Note Title')
        self.assertEqual(note.__str__(), 'Note Title') and self.assertEqual(note.body, 'this is the note body')