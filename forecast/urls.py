from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_luas_times, name="forecast_home"),
    path("api/luas/<str:stop_id>", views.luas_times_json, name="luas_times_json"),
]
