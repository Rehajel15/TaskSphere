from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.main, name='main'),
    path('signin/', views.SignIn, name='signin'),
    path('signup/', views.SignUp, name='signup'),
    path('choosegroupaction', views.ChooseGroupAction, name='choosegroupaction'),
    path('joingroup/', views.JoinGroup, name='joingroup'),
    path('creategroup/', views.CreateGroup, name='creategroup'),
    path('leavegroup/', views.LeaveGroup, name='leavegroup'),
    path('deleteacc/', views.DeleteAccount, name='deleteaccount'),
    path('signout/', views.SignOut, name='signout'),
]