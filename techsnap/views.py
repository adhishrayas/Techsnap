from django.shortcuts import render,redirect


def custom_404(request, exception):
    return render(request, '404.html', status=404)
from django.shortcuts import redirect

def redirect_to_specific_url(request):
    return redirect('Authmodules:login') 
