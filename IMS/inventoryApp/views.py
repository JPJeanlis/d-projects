from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'inventoryApp/index.html', {})

def base_generic(request):
    return render(request, 'inventoryApp/base_generic.html', {})
