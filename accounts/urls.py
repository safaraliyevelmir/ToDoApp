from django.urls import path

from accounts.views import  activate, RegisterView, loginUser, logoutUser


urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',loginUser,name="login"),
    path('activate/<str:token>/',activate,name='activate'),
    path('logout/',logoutUser,name='logout')
]
