from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseServerError
from .models import Receipts, Item
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from _datetime import datetime
from django.core.serializers import serialize
from .processors import sync as sync_processor
from oauth.credentials import google_credentials

import base64


import json

def index(request):
    return render(request, 'receipts/receipts.html')

def pickup(request):
    return render(request, 'receipts/pickup.html')

@csrf_exempt
def pickup_endpoint(request):
    def parse_json():
        received_json_data=json.loads(request.body.decode('utf-8'))
        raw = received_json_data['raw_content']
        name = received_json_data['name']
        user = received_json_data['user']
        return user, name, raw

    def parse_form():
        raw = request.POST['raw_content']
        name = request.POST['name']
        user = request.POST['user']
        return user, name, raw

    try:
        user, name, raw = parse_json()
    except Exception as e1:
        try:
            user, name, raw = parse_form()
        except Exception as e2:
            print(e1)
            print(e2)

    rc = base64.urlsafe_b64decode(raw).decode('unicode_escape')
    rdate = datetime.strptime(rc.split("\r\n")[2].strip(), '%a, %d %b %Y %H:%M:%S %z (%Z)')
    r = Receipts(receipts_name=name, receipts_date=rdate, raw_content=rc, user=user)
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

    filter_p = {'invalid': False}
    if 'name' in received_json_data:
        filter_p['receipts_name__startswith']=received_json_data['name']
    if 'from' in received_json_data:
        filter_p['receipts_date__gt']=received_json_data['from']
    if 'to' in received_json_data:
        filter_p['receipts_date__lt']=received_json_data['to']

    order_by = received_json_data['order_by'] if 'order_by' in received_json_data else '-receipts_date'
    page_start = received_json_data['page_start'] if 'page_start' in received_json_data else 0
    page_size = received_json_data['page_size'] if 'page_size' in received_json_data else 1000000

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


def sync(request):
    if 'google_user' not in request.session or request.session['google_user'] not in google_credentials:
        return HttpResponseServerError('Please login first')

    user = request.session['google_user']
    sync_processor.sync(user)
    return HttpResponse('Success')


