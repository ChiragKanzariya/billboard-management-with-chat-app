from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
import datetime 
import numpy as np

from advertiser.models import Post, Invitation
from advertiser.forms import PostForm, InvitationForm, SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('advertiser_home')  
    else:
        form = SignUpForm()
    return render(request, 'advertiser/signup_form.html', {'form': form})

@login_required()
def home(request):
    post_list = Post.objects.all() 
    return render(request, 'advertiser/home.html', {'lists': post_list})

@login_required
def billboard_owner(request):
    if not request.user.is_staff == True:
        return HttpResponse('You are not Authorized for this URL!')
    else:
        invitations = request.user.invitations_received.all()
        return render(request, 'advertiser/owner.html',{'invitations': invitations})

@login_required
def post_new(request):
    owner = Invitation.objects.all()
    if request.method == "POST":
        form = InvitationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('advertiser_home')
    else:
        form = InvitationForm()   
    return render(request, 'advertiser/post_edit.html', {'form': form})

@login_required()
def new_invitation(request):
    if request.method == "POST":
        invitation = Invitation(from_author=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('advertiser_home')
    else: 
        form = InvitationForm()
    return render(request, "advertiser/new_invitation_form.html", {'form': form})

@login_required()
def accept_invitation(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_owner:
        raise PermissionDenied

    if request.method == "POST":
        if "accept" in request.POST:

            diff = int(invitation.date_from.strftime('%d')) - int(invitation.date_to.strftime('%d'))
            all_date = np.array([invitation.date_to + datetime.timedelta(days=i) for i in range(diff+1) ])

            for i in range(diff+1):
                post = Post.objects.create(
                    owner=invitation.to_owner,
                    author=invitation.from_author,
                    title=invitation.title,
                    clip=invitation.clip,
                    date_to=all_date[i],
                    time_to=invitation.time_to,
                    date_from=all_date[i],
                    time_from=invitation.time_from
                )
        invitation.delete()
        return redirect('advertiser_owner_home')
    else:   
        return render(request, 
                      "advertiser/accept_invitation_form.html",
                      {'invitation': invitation}  
                     )

@login_required    
@require_GET
def notification(request, id):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = get_object_or_404(Invitation, pk=id)
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

        return JsonResponse(status=200, data={'message': 'Web push successful'})
    except TypeError:
        return JsonResponse(status=500, data={'message': 'Error occurred.'})


