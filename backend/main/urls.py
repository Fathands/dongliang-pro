from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('api/get_wencai_data/', views.get_wencai_data, name='get_wencai_data'),
]