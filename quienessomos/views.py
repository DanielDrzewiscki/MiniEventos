from django.shortcuts import render,redirect


# Create your views here.

def quienessomos(request):
   
    return render(request, 'quienessomos/quienessomos.html')