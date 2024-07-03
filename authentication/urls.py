from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.main, name='main'),
    path('signin/', views.SignIn, name='signin'),
    path('signup/', views.SignUp, name='signup'),
    path('signup/joingroup/', views.JoinGroup, name='joingroup'),
    path('signout/', views.SignOut, name='signout')
]