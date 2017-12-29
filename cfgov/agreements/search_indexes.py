from haystack import indexes

from agreements.models import Agreement, Issuer, PrepayAgreement


class IssuerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        model_attr='name')
    autocomplete = indexes.EdgeNgramField(
        model_attr='name')

    def get_model(self):
        return Issuer

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(agreement=None)


class AgreementIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        # model_attr='plan__name',  # use when SalesForce data become available
        model_attr='description',
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        # model_attr='plan__name')
        model_attr='description')
    uri = indexes.CharField(
        model_attr='uri',
        indexed=False)
    issuer_name = indexes.CharField(
        model_attr='issuer__name',
        indexed=True)
    issuer_slug = indexes.CharField(
        model_attr='issuer__slug',
        indexed=True)
    issuer_pk = indexes.IntegerField(
        model_attr='issuer__pk',
        indexed=True)
    # initial_date = indexes.DateTimeField(
    #     model_attr='plan__offered',
    #     indexed=True)
    # withdrawn_date = indexes.DateTimeField(
    #     model_attr='plan__withdrawn',
    #     indexed=True)
    effective = indexes.DateTimeField(
        indexed=True,
        # model_attr='offered')
        model_attr='posted')

    def get_model(self):
        return Agreement

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(issuer=None)


class PrepayAgreementIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        model_attr='plan__name',
        boost=10.0)
    autocomplete = indexes.EdgeNgramField(
        model_attr='plan__name',
        indexed=True)
    uri = indexes.CharField(
        model_attr='uri',
        indexed=False)
    plan_type = indexes.CharField(
        model_attr='plan__plan_type',
        indexed=True)
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
        model_attr='plan__offered',
        indexed=True)
    withdrawn_date = indexes.DateTimeField(
        model_attr='plan__withdrawn',
        indexed=True)
    effective = indexes.DateTimeField(
        indexed=True,
        # model_attr='offered')
        model_attr='posted')

    def get_model(self):
        return PrepayAgreement

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
