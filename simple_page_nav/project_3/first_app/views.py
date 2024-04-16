from django.shortcuts import render
import datetime
# Create your views here.
def home(request):
    d={
        'author':'Rahim', 'age':12, 'lst' : ['python','is','best'],'birthday' :datetime.datetime.now(), 'val' : '' , 'courses':[
    {'id':1,'name':'Python','fees':2000},{'id':2,'name':'django','fees':3000},{'id':3,'name':'devops','fees':3000}]
        

    }
    return render(request, 'home.html',d)