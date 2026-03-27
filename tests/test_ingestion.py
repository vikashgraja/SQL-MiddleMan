import pytest
from rest_framework import status

@pytest.mark.django_db
def test_ingestion_insert_and_fetch(auth_client):
    # 1. Insert Data
    insert_url = "/ingestion/sample_data/insert/"
    payload = {
        "run_id": "test_run_pytest",
        "rows": [{"dummy_val": "pytest_val"}]
    }
    response = auth_client.post(insert_url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "success"

    # 2. Fetch Data
    fetch_url = "/ingestion/sample_data/fetch/"
    response = auth_client.get(fetch_url, {"run_id": "test_run_pytest"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    assert response.data[0]["run_id"] == "test_run_pytest"
