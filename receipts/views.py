from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Receipts
from django.urls import reverse

def index(request):
    latest_receipts_list = Receipts.objects.order_by('-receipts_date')[:5]
    context = {
        'latest_receipts_list': latest_receipts_list,
    }
    return render(request, 'receipts/index.html', context)

def pickup(request):
    return render(request, 'receipts/pickup.html')

def pickup_endpoint(request):
    try:
        raw_content = request.POST['raw_content']
    except:
        # TODO: handle error
        pass
    else:
        # TODO: process raw content
        print(raw_content)
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
