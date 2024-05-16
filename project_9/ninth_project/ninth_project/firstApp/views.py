from django.shortcuts import render
from datetime import datetime,timedelta
from django.http import HttpResponse

# Create your views here.
def home(request):
    response=render(request, 'home.html')
    # response.set_cookie('name','rahim',max_age=10)
    response.set_cookie('name','rahim', expires=datetime.utcnow()+timedelta(days=7))
    return response
def get_cookie(request):
    name=request.COOKIES.get('name')
    print(request.COOKIES)
    return render(request, 'get_cookie.html',{'name':name})

def delete_cookie(request):
    response=render(request, 'delete_cookie.html')
    response.delete_cookie('name')
    return response

def set_session(request):
    data={
        'name':'meem',
        'age':20,
        'lang':'Bangla'
    }
    print(request.session.get_session_cookie_age())
    print(request.session.get_expiry_date())

    request.session.update(data)
    return render(request, 'home.html')

# def get_session(request):
#     name=request.session.get('name','Guest')
#     age=request.session.get('age','00')

#     return render(request, 'get_session.html',{'name':name, 'age':age})


def delete_session(request):
    # del request.session['name']

    #whole session is deleted
    request.session.flush()
    return render(request, 'delete.html')

def get_session(request):
   if 'name' in request.session:
       name=request.session.get('name','Guest')
       request.session.modified=True
       return render(request, 'set_session.html',{'name':name})
   else:
       return HttpResponse("Your session has been expired.Login again")