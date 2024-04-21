from django.urls import path,include
from . import views
app_name = "home"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('predict',views.predict,name='predict'),
    path('crimestatistics',views.crimestatistics,name='crimestatistics'),
    path('scam_report',views.scam_report,name="submit_scam_report"),
    path('check-user-type', views.check_user_type, name="check_user_type"),
    path('check-user-type-signup', views.check_user_type_signup, name="check_user_type"),
    path('display_scam_reports',views.display_scam_reports,name="display_scam_reports"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

