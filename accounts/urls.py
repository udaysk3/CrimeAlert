from django.urls import path
from .views import police_signup, police_login, police_logout, change_district


urlpatterns = [
    path('police/signup/', police_signup, name='police_signup'),
    path('police/login/', police_login, name='police_login'),
    path('police/logout/', police_logout, name='police_logout'),
    path('change_district',change_district,name="change_district")
]