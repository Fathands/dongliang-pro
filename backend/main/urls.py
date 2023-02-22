from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("api/get_wencai_data", views.get_wencai_data, name="get_wencai_data"),
    path("api/get_all_date", views.get_all_date, name="get_all_date"),
    path("api/get_years_data", views.get_years_data, name="get_years_data"),
]
