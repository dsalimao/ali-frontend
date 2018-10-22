from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Receipts
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from _datetime import datetime
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
    r = Receipts(receipts_name=name, receipts_date=rdate, raw_content=raw)
    r.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('receipts:pickup'))


def detail(request, receipts_id):
    receipts = get_object_or_404(Receipts, pk=receipts_id)
    return render(request, 'receipts/detail.html', {'receipts': receipts})

def raw(request, receipts_id):
    response = "You're looking at the raw content of receipts %s."
    return HttpResponse(response % receipts_id)
