from data_center.models import Course
from haystack import indexes


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)

    no = indexes.CharField(model_attr='no')
    code = indexes.CharField(model_attr='code')
    eng_title = indexes.CharField(model_attr='eng_title')
    chi_title = indexes.CharField(model_attr='chi_title')
    note = indexes.CharField(model_attr='note')
    objective = indexes.CharField(model_attr='objective')
    time = indexes.CharField(model_attr='time')
    time_token = indexes.CharField(model_attr='time_token')
    teacher = indexes.CharField(model_attr='teacher')
    room = indexes.CharField(model_attr='room')
    ge = indexes.CharField(model_attr='ge')

    credit = indexes.IntegerField(model_attr='credit')
    limit = indexes.IntegerField(model_attr='limit')
    prerequisite = indexes.BooleanField(model_attr='prerequisite')

    ys = indexes.CharField(model_attr='ys')

    hit = indexes.IntegerField(model_attr='hit')

    syllabus = indexes.CharField(model_attr='syllabus')

    def get_model(self):
        return Course
