from __future__ import unicode_literals
from django.db import models


class CreditBase(models.Model):
    """An abstract base class for all credit-card and prepay models."""
    name = models.TextField(max_length=500)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class Issuer(CreditBase):
    med_id = models.IntegerField(blank=True, null=True)

    @property
    def payload(self):
        return {'name': self.name, 'slug': self.slug, 'pk': self.pk}


class CreditPlan(CreditBase):
    issuer = models.ForeignKey(Issuer)
    offered = models.DateField(blank=True, null=True)
    withdrawn = models.DateField(blank=True, null=True)

    @property
    def payload(self):
        return {'name': self.name,
                'pk': self.pk,
                'issuer': "{}".format(self.issuer),
                'offered': '{}'.format(self.offered),
                'withdrawn': '{}'.format(self.withdrawn)}


class PrepayPlan(CreditBase):
    issuer = models.ForeignKey(Issuer)
    offered = models.DateField(blank=True, null=True)
    withdrawn = models.DateField(blank=True, null=True)
    plan_type = models.CharField(max_length=255, blank=True)

    @property
    def payload(self):
        return {'name': self.name,
                'pk': self.pk,
                'issuer': "{}".format(self.issuer),
                'offered': '{}'.format(self.offered),
                'withdrawn': '{}'.format(self.withdrawn),
                'plan_type': self.plan_type}


class AgreementBase(models.Model):
    issuer = models.ForeignKey(Issuer, null=True)
    file_name = models.TextField(
        max_length=500, help_text='To support legacy processing')
    size = models.IntegerField()
    uri = models.URLField(max_length=500)
    description = models.TextField(
        blank=True, help_text='To support legacy processing')
    offered = models.DateField(blank=True, null=True)
    withdrawn = models.DateField(blank=True, null=True)
    posted = models.DateField(
        null=True,
        help_text='For legacy PDFs, this is the S3 posting date; '
                  'for SalesForce PDFs, this is the uploaded date')

    def __str__(self):
        return self.file_name

    class Meta:
        abstract = True
        ordering = ['-posted']

    @property
    def payload(self):
        return {'issuer': "{}".format(self.issuer),
                'size': self.size,
                'uri': self.uri,
                'offered': '{}'.format(self.offered),
                'withdrawn': '{}'.format(self.withdrawn),
                'posted': '{}'.format(self.posted)}


class Agreement(AgreementBase):
    plan = models.ForeignKey(CreditPlan, null=True)
    legacy = models.BooleanField(
        default=False, help_text='Marker for pre-SalesForce PDFs')

    @property
    def payload(self):
        data = super(Agreement, self).payload
        if self.plan:
            data.update({'plan': self.plan.name, 'pk': self.pk})
        else:
            data.update({'plan': None, 'pk': self.pk})

        return data


class PrepayAgreement(AgreementBase):
    plan = models.ForeignKey(PrepayPlan, null=True)

    @property
    def payload(self):
        data = super(PrepayAgreement, self).payload
        if self.plan:
            data.update({'plan': self.plan.name, 'pk': self.pk})
        else:
            data.update({'plan': None, 'pk': self.pk})
        return data
