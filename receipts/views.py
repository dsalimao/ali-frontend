from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Receipts, Item
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from _datetime import datetime
from django.core.serializers import serialize
import base64

import json

def index(request):
    latest_receipts_list = Receipts.objects.order_by('-receipts_date')[:5]
    context = {
        'latest_receipts_list': latest_receipts_list,
    }
    return render(request, 'receipts/receipts.html', context)

def pickup(request):
    return render(request, 'receipts/pickup.html')

@csrf_exempt
def pickup_endpoint(request):
    def parse_json():
        received_json_data=json.loads(request.body.decode('utf-8'))
        raw = received_json_data['raw_content']
        name = received_json_data['name']
        return name, raw

    def parse_form():
        raw = request.POST['raw_content']
        name = request.POST['name']
        return name, raw

    try:
        name, raw = parse_json()
    except Exception as e1:
        try:
            name, raw = parse_form()
        except Exception as e2:
            print(e1)
            print(e2)

    rdate = datetime.now()
    r = Receipts(receipts_name=name, receipts_date=rdate, raw_content=base64.urlsafe_b64decode(raw))
    r.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('receipts:pickup'))


def search_receipts(request):
    """
    Searches all receipts. This is a POST method, accept JSON data only.
    """
    received_json_data=json.loads(request.body.decode('utf-8'))
    print(received_json_data)

    filter_p = {}
    if 'name' in received_json_data:
        filter_p['receipts_name__startswith']=received_json_data['name']
    if 'from' in received_json_data:
        filter_p['receipts_date__gt']=received_json_data['from']
    if 'to' in received_json_data:
        filter_p['receipts_date__lt']=received_json_data['to']

    order_by = received_json_data['order_by'] if 'order_by' in received_json_data else '-receipts_date'
    page_start = received_json_data['page_start'] if 'page_start' in received_json_data else 0
    page_size = received_json_data['page_size'] if 'page_size' in received_json_data else 10

    receipts_list = Receipts.objects.filter(**filter_p).order_by('-receipts_date')[page_start:page_start + page_size]
    data_s = json.loads(serialize('json', receipts_list, fields=('receipts_name', 'receipts_date', 'total_price')))

    def to_json_line(r):
        j = r['fields']
        j['id'] = r['pk']
        return j

    data = list(map(to_json_line,data_s))
    return JsonResponse({'payload': data})


def get_detail(request, receipts_id):
    items = Item.objects.filter(receipts_id=receipts_id)
    data_s = json.loads(serialize('json', items))

    def to_json_line(i):
            j = i['fields']
            j['id'] = i['pk']
            return j

    data = list(map(to_json_line,data_s))
    return JsonResponse({'payload': data})


def get_raw(request, receipts_id):
    receipts = Receipts.objects.get(pk=receipts_id)
    return JsonResponse({'payload': receipts.raw_content})
