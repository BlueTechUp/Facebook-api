from django.http import JsonResponse
from django.shortcuts import render
from home.restAPI.facebookAPI import check_ad


# Create your views here.

def home(request):
    return render(request, 'home/layout.html')


def check(request):
    token = request.GET['token']
    check_data = check_ad(token)
    return JsonResponse({'aaData': check_data})

