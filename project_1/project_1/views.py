from django.http import HttpResponse

def contact(request):
    return HttpResponse("This is contact page")

def home(request):
    return HttpResponse("This is home page")