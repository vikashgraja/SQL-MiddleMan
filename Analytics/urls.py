from django.urls import path
from .api.sample_result_api import insert_sample_result_api, fetch_sample_result_api

urlpatterns = [
    path("sample_result/insert/", insert_sample_result_api),
    path("sample_result/fetch/", fetch_sample_result_api),
]
