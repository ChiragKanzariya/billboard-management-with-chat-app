from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
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
    post_len = Post.objects.count()
    post = Post.objects.all()
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
def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })




