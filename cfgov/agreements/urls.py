from django.conf.urls import url

from agreements.views import (
    agreement_autocomplete, agreement_search, CreditDataView,
    index, legacy_issuer_search
)


urlpatterns = [
    url(r'^$', index, name='agreements_home'),
    url(r'^issuer/(?P<issuer_slug>.*)/$',
        legacy_issuer_search,
        name='legacy_issuer_search'),
    url(r'^api/(?P<model>credit-agreement)/search/?$',
        agreement_search,
        name='agreement-search'),
    url(r'^api/(?P<model>prepay-agreement)/search/?$',
        agreement_search,
        name='prepay-agreement-search'),
    url(r'^api/(?P<model>issuer)/search/?$',
        agreement_search,
        name='issuer-search'),
    url(r'^api/(?P<model>credit-agreement)/autocomplete/?$',
        agreement_autocomplete, name='credit-agreement-autocomplete'),
    url(r'^api/(?P<model>prepay-agreement)/autocomplete/?$',
        agreement_autocomplete, name='prepay-agreement-autocomplete'),
    url(r'^api/(?P<model>issuer)/autocomplete/?$',
        agreement_autocomplete, name='issuer-autocomplete'),
    url(r'^api/(?P<model>.*)/(?P<pk>\d{1,12})/?$',
        CreditDataView.as_view(), name='agreement-credit-data'),
]
