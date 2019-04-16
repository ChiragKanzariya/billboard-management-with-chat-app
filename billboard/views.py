from django.shortcuts import render, redirect

def welcome(request):
    if request.user.is_authenticated:
        return redirect ('advertiser_home')
    else:
        return render(request, 'billboard/welcome.html') 