from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

def welcome(request):
    if request.user.is_authenticated:
        return redirect ('advertiser_home')
    else:
        return render(request, 'billboard/welcome.html') 

@login_required    
@require_GET
def notification(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    return render(request, 'advertiser/notification/notification.html', {user: user, 'vapid_key':vapid_key})

@login_required
@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={'message': 'Invalid data enter valid data.'})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        print(payload)
        send_user_notification(user=user, payload=payload, ttl=1000)
        print(payload)

        return JsonResponse(status=200, data={'message': 'Web push successful'})
    except TypeError:
        return JsonResponse(status=500, data={'message': 'Error occurred.'})