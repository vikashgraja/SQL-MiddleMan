from django.urls import path
from .api.sample_data_api import insert_sample_data_api, fetch_sample_data_api

urlpatterns = [
    path("sample_data/insert/", insert_sample_data_api),
    path("sample_data/fetch/", fetch_sample_data_api),
]
