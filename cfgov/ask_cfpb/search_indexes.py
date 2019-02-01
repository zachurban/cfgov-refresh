from haystack import indexes

from ask_cfpb.models import AnswerPage, Category
from search import fields


# AnswerTagProxy,


class AnswerPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = fields.CharFieldWithSynonyms(
        document=True,
        use_template=True,
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        use_template=True,
        indexed=True)
    url = indexes.CharField(
        use_template=True,
        indexed=False)
    tags = indexes.MultiValueField(
        indexed=True,
        boost=10.0)
    last_edited = indexes.DateTimeField(
        indexed=True,
        null=True,
        model_attr='last_edited',
        boost=2.0)
    suggestions = indexes.FacetCharField()

    def prepare_tags(self, obj):
        return obj.clean_tags

    def prepare_answer(self, obj):
        data = super(AnswerPageIndex, self).prepare(obj)
        if obj.question.lower().startswith('what is'):
            data['boost'] = 2.0
        return data

    def prepare(self, obj):
        data = super(AnswerPageIndex, self).prepare(obj)
        data['suggestions'] = data['text']
        return data

    def get_model(self):
        return AnswerPage

    def index_queryset(self, using=None):
        ids = [page.id for page in self.get_model().objects.all()
               if page.live is True
               and page.redirect_to is None]
        return self.get_model().objects.filter(id__in=ids)


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True)
    facet_map = indexes.CharField(
        indexed=True)
    slug = indexes.CharField(
        model_attr='slug')
    slug_es = indexes.CharField(
        model_attr='slug_es')

    def prepare_facet_map(self, obj):
        return obj.facet_map

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


# class TagIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(
#         use_template=True,
#         document=True)

#     valid_spanish = indexes.MultiValueField()

#     def get_model(self):
#         return AnswerTagProxy

#     def prepare_valid_spanish(self, obj):
#         return self.get_model().valid_spanish_tags()

#     def index_queryset(self, using=None):
#         return self.get_model().objects.filter(id=1)
