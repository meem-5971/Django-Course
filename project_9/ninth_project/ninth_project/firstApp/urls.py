from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.set_session),
    path('get/',views.get_session),
    # path('get/',views.get_cookie),
    # path('del/',views.delete_cookie)
    path('del/',views.delete_session),
    path('set/',views.set_session)
]