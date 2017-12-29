from __future__ import unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render
from haystack.inputs import Clean
from haystack.query import SearchQuerySet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from agreements import RESULTS_PER_PAGE
from agreements.models import (
    Agreement, CreditPlan, Issuer, PrepayAgreement, PrepayPlan
)


MODEL_MAP = {
    'credit-agreement': Agreement,
    'credit-plan': CreditPlan,
    'issuer': Issuer,
    'prepay-agreement': PrepayAgreement,
    'prepay-plan': PrepayPlan,
}


def index(request):
    return render(request, 'agreements/index.html', {
        'agreement_count': Agreement.objects.all().count(),
        'pagetitle': 'Credit card agreements',
    })


def legacy_issuer_search(request, issuer_slug):
    issuers = Issuer.objects.filter(slug=issuer_slug)

    if not issuers.exists():
        raise Http404

    agreements = Agreement.objects.filter(issuer__in=issuers)

    if agreements.exists():
        issuer = agreements.latest('pk').issuer
    else:
        issuer = issuers.latest('pk')

    pager = Paginator(
        agreements.order_by('-posted', 'description'),
        RESULTS_PER_PAGE
    )

    try:
        page = pager.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = pager.page(1)
    except EmptyPage:
        page = pager.page(pager.num_pages)

    return render(request, 'agreements/search.html', {
        'page': page,
        'issuer': issuer,
    })


def agreement_search(request, model):
    search_model = MODEL_MAP.get(model)
    clean_query = Clean(request.GET.get('q', ''))
    qstring = clean_query.query_string.strip()
    if not qstring or not search_model:
        raise Http404
    sqs = SearchQuerySet().models(search_model)
    search = sqs.filter(content=clean_query)

    results = [{'agreement': result.autocomplete,
                'pk': result.pk,
                'uri': result.uri,
                'issuer': "{}".format(result.issuer),
                'issuer_slug': result.issuer.slug if result.issuer else None,
                'posted': result.posted}
               for result in search]
    return JsonResponse(results, safe=False)


def agreement_autocomplete(request, model):
    search_model = MODEL_MAP.get(model)
    term = request.GET.get(
        'term', '').strip().replace('<', '')
    if not term or not search_model:
        return JsonResponse([], safe=False)
    sqs = SearchQuerySet().models(search_model).autocomplete(autocomplete=term)
    results = [{'name': result.autocomplete,
                'pk': result.pk}
               for result in sqs[:20]]

    return JsonResponse(results, safe=False)


class CreditDataView(APIView):
    """
    API view for delivering credit objects by primary key
    """
    renderer_classes = (JSONRenderer,)

    def get(self, request, model, pk):
        search_model = MODEL_MAP.get(model)
        if not search_model or not pk:
            raise Http404("Invalid model")
        try:
            result = search_model.objects.get(pk=pk)
        except search_model.DoesNotExist:
            raise Http404("No {} found.".format(model))
        return Response(result.payload)
