# authentication/urls.py
from django.urls import path
from .views import signup, user_login, home,user_logout,profile_page,view_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='logout'), 
    path('profile/', profile_page, name='profile_page'),  # Add this line for the profile page
    path('view_profile/<int:user_id>/', view_profile, name='view_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
