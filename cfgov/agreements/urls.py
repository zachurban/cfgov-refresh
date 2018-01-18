from django.conf.urls import url

from agreements.views import (
    api_root,
    autocomplete,
    CreditDataView,
    index,
    legacy_issuer_search,
    plan_search
)

urlpatterns = [
    url(r'^$', index, name='agreements_home'),
    url(r'^issuer/(?P<issuer_slug>.*)/$',
        legacy_issuer_search,
        name='legacy_issuer_search'),
    url(r'^api/?$',
        api_root,
        name='api-root'),
    url(r'^api/(?P<model>credit)/search/?$',
        plan_search,
        name='credit-search'),
    url(r'^api/(?P<model>prepay)/search/?$',
        plan_search,
        name='prepay-search'),
    url(r'^api/(?P<model>credit)/autocomplete/?$',
        autocomplete, name='credit-autocomplete'),
    url(r'^api/(?P<model>prepay)/autocomplete/?$',
        autocomplete, name='prepay-autocomplete'),
    url(r'^api/(?P<model>issuer)/autocomplete/?$',
        autocomplete, name='issuer-autocomplete'),
    url(r'^api/(?P<model>.*)/(?P<pk>\d{1,12})/?$',
        CreditDataView.as_view(), name='agreement-credit-data'),
]
