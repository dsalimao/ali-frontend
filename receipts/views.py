from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Receipts
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .processors.pickup import on_pickup
import json

def index(request):
    latest_receipts_list = Receipts.objects.order_by('-receipts_date')[:5]
    context = {
        'latest_receipts_list': latest_receipts_list,
    }
    return render(request, 'receipts/index.html', context)

def pickup(request):
    return render(request, 'receipts/pickup.html')

@csrf_exempt
def pickup_endpoint(request):
    try:
        received_json_data=json.loads(request.body.decode('utf-8'))
        raw_content = received_json_data['raw_content']
        name = received_json_data['name']
    except Exception as e:
        # TODO: handle error
        print(e)
        pass
    else:
        # TODO: process raw content
        on_pickup(name, raw_content)
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
