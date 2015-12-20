from django.test import TestCase

from data_center.models import Course, FlatPrerequisite


class CourseModelTest(TestCase):

    def test_course_can_be_created_with_only_no(self):
        Course.objects.create(no='12345QAQ 010101')

        self.assertEqual(1, Course.objects.count())


class FlatPrerequisiteModelTest(TestCase):

    def test_update_html_creates_object(self):
        FlatPrerequisite.update_html('<3')
        self.assertEqual(FlatPrerequisite.objects.count(), 1)

        self.assertEqual(FlatPrerequisite.objects.get().html, '<3')

    def test_update_html_updates_object(self):
        FlatPrerequisite.update_html('<3')

        FlatPrerequisite.update_html('<4')

        self.assertEqual(FlatPrerequisite.objects.count(), 1)
        self.assertEqual(FlatPrerequisite.objects.get().html, '<4')
