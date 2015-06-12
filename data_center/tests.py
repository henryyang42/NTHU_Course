from django.test import TestCase

from data_center.models import Course


class ModelTest(TestCase):

    def test_course_can_be_created_with_only_no(self):
        Course.objects.create(no='12345QAQ 010101')

        self.assertEqual(1, Course.objects.count())

    def test_this_test_shall_fail(self):
        self.fail()
