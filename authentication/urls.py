# authentication/urls.py
from django.urls import path
from .views import signup, user_login, home,user_logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='logout'), 
]
