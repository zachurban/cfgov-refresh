from __future__ import unicode_literals
import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from haystack.query import SearchQuerySet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from agreements import RESULTS_PER_PAGE
from agreements.models import (
    Agreement, CreditPlan, Issuer, PrepayPlan
)

MODEL_MAP = {
    'issuer': Issuer,
    'credit': CreditPlan,
    'prepay': PrepayPlan
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


def clean_ids(id_strings):
    """Convert a list of id strings to ints"""
    pks = []
    if not id_strings:
        return pks
    for id_string in id_strings:
        try:
            pk = int(id_string)
        except:
            pass
        else:
            pks.append(pk)
    return pks


def clean_queries(query_strings):
    """Disable brackets and disallow excessively long queries in list"""
    q_strings = []
    if not query_strings:
        return q_strings
    for q_string in query_strings:
        q_strings.append(q_string.replace('>', '')[:50])
    return q_strings


def plan_search(request, model):
    """Search collects credit or prepay plans by id and/or issuer query)"""
    search_model = MODEL_MAP.get(model)
    if not search_model:
        raise HttpResponseBadRequest("Invalid model")
    issuer_query_strings = (request.GET.getlist('q', ''))
    issuer_queries = clean_queries(issuer_query_strings)
    plan_id_strings = (request.GET.getlist('plan_id', ''))
    plan_ids = clean_ids(plan_id_strings)
    if not plan_ids and not issuer_queries:
        return JsonResponse({})
    if issuer_queries:
        for query in issuer_queries:
            for result in SearchQuerySet().models(Issuer).filter(
                    content=query):
                plan_ids += json.loads(result.plan_ids)

    plans = search_model.objects.filter(pk__in=set(plan_ids))
    results = [plan.payload for plan in plans]
    return JsonResponse({'data': results})


def autocomplete(request, model):
    """Return issuer or plan suggestions based on word fragments"""
    search_model = MODEL_MAP.get(model)
    if not search_model:
        raise HttpResponseBadRequest("Invalid model")
    term = request.GET.get('term', '').strip().replace('>', '')[:50]
    if not term:
        return JsonResponse([], safe=False)
    sqs = SearchQuerySet().models(
        search_model).autocomplete(autocomplete=term)
    if model == 'issuer':
        results = sorted([{'name': result.autocomplete,
                           'pk': result.pk,
                           'plan_ids': json.loads(result.plan_ids)}
                         for result in sqs[:20]], key=lambda k: k['name'])
    else:
        results = sorted([{'name': result.autocomplete,
                           'plan_id': result.pk}
                          for result in sqs[:20]], key=lambda k: k['name'])

    return JsonResponse({'data': results})


class CreditDataView(APIView):
    """
    API view for delivering credit objects by primary key
    """
    renderer_classes = (JSONRenderer,)

    def get(self, request, model, pk):
        search_model = MODEL_MAP.get(model)
        if not search_model or not pk:
            raise HttpResponseBadRequest("Invalid model or key")
        try:
            result = search_model.objects.get(pk=pk)
        except search_model.DoesNotExist:
            raise Http404("No {} found.".format(model))
        return Response(result.payload)
