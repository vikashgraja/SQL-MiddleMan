import pytest
from rest_framework import status

@pytest.mark.django_db
def test_analytics_insert_and_fetch(auth_client):
    # 1. Insert Result
    insert_url = "/analytics/sample_result/insert/"
    payload = {
        "run_id": "test_run_analytics",
        "rows": [{"dummy_val": "result_val"}]
    }
    response = auth_client.post(insert_url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "success"

    # 2. Fetch Result
    fetch_url = "/analytics/sample_result/fetch/"
    response = auth_client.get(fetch_url, {"run_id": "test_run_analytics"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    assert response.data[0]["run_id"] == "test_run_analytics"
