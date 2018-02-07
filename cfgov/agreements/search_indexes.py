import json
from haystack import indexes

from agreements.models import CreditPlan, Issuer, PrepayPlan


class IssuerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        model_attr='name')
    autocomplete = indexes.EdgeNgramField(
        model_attr='name')
    slug = indexes.CharField(
        model_attr='slug')
    plan_ids = indexes.CharField()

    def get_model(self):
        return Issuer

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(creditplan=None)

    def prepare_plan_ids(self, obj):
        return json.dumps(obj.plan_ids)


class CreditPlanIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        model_attr='name')
    issuer_name = indexes.CharField(
        model_attr='issuer__name',
        indexed=True)
    issuer_slug = indexes.CharField(
        model_attr='issuer__slug',
        indexed=True)
    issuer_pk = indexes.IntegerField(
        model_attr='issuer__pk',
        indexed=True)
    initial_date = indexes.DateTimeField(
        model_attr='offered',
        indexed=True)
    withdrawn_date = indexes.DateTimeField(
        model_attr='withdrawn',
        null=True)

    def get_model(self):
        return CreditPlan

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(agreement=None)


class PrepayPlanIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        model_attr='name')
    issuer_name = indexes.CharField(
        model_attr='issuer__name',
        indexed=True)
    issuer_slug = indexes.CharField(
        model_attr='issuer__slug',
        indexed=True)
    issuer_pk = indexes.IntegerField(
        model_attr='issuer__pk',
        indexed=True)
    initial_date = indexes.DateTimeField(
        model_attr='offered',
        indexed=True)
    withdrawn_date = indexes.DateTimeField(
        model_attr='withdrawn',
        null=True)
    plan_type = indexes.CharField(
        model_attr='plan_type',)

    def get_model(self):
        return PrepayPlan

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
