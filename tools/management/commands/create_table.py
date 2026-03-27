import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create model, service, and api files for a table"

    def add_arguments(self, parser):
        parser.add_argument("app")
        parser.add_argument("name")

    def handle(self, *args, **kwargs):
        app = kwargs["app"]
        name = kwargs["name"].lower()
        class_name = "".join(word.capitalize() for word in name.split("_"))

        base_path = app

        model_path = f"{base_path}/models/{name}.py"
        serializer_path = f"{base_path}/serializers/{name}_serializer.py"
        service_path = f"{base_path}/services/{name}_service.py"
        api_path = f"{base_path}/api/{name}_api.py"
        test_path = f"{base_path}/tests/test_{name}.py"

        files = {
            model_path: self.model_template(class_name, name),
            serializer_path: self.serializer_template(class_name, name),
            service_path: self.service_template(name),
            api_path: self.api_template(class_name, name),
            test_path: self.test_template(app, name),
        }

        # Create files
        for path, content in files.items():
            os.makedirs(os.path.dirname(path), exist_ok=True)

            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
                self.stdout.write(self.style.SUCCESS(f"Created {path}"))
            else:
                self.stdout.write(self.style.WARNING(f"{path} already exists"))

        self.update_init(app, name)

    def update_init(self, app, name):
        init_file = f"{app}/models/__init__.py"
        import_line = f"from .{name} import *\n"

        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write(import_line)
            self.stdout.write(self.style.SUCCESS(f"Created {init_file}"))
            return

        with open(init_file, "r") as f:
            content = f.readlines()

        if import_line not in content:
            with open(init_file, "a") as f:
                f.write(import_line)
            self.stdout.write(self.style.SUCCESS(f"Updated {init_file}"))
        else:
            self.stdout.write(self.style.WARNING(f"{init_file} already updated"))

    def model_template(self, class_name, name):
        return f"""from django.db import models


class {class_name}(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    run_id = models.CharField(max_length=50)

    class Meta:
        db_table = "{name}"

"""

    def serializer_template(self, class_name, name):
        return f"""from rest_framework import serializers

class {class_name}Serializer(serializers.Serializer):
    # TODO: define fields
    pass
"""

    def service_template(self, name):               # TODO: Use serializers
        return f"""def insert_{name}(rows, run_id):
    # TODO: implement logic
    pass

def fetch_{name}(run_id=None):
    # TODO: implement logic
    return []
"""

    def api_template(self, class_name, name):
        return f"""from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..services.{name}_service import insert_{name}, fetch_{name}
from ..serializers.{name}_serializer import {class_name}Serializer


# -------- INSERT --------
@api_view(["POST"])
def insert_{name}_api(request):
    serializer = {class_name}Serializer(
        data=request.data.get("rows", []), many=True
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    insert_{name}(
        rows=serializer.validated_data,
        run_id=request.data.get("run_id")
    )

    return Response({{"status": "success"}})


# -------- FETCH --------
@api_view(["GET"])
def fetch_{name}_api(request):
    run_id = request.GET.get("run_id")

    data = fetch_{name}(run_id=run_id)

    serializer = {class_name}Serializer(data, many=True)

    return Response(serializer.data)
"""

    def test_template(self, app, name):
        return f"""import pytest
from rest_framework import status

@pytest.mark.django_db
def test_{name}_insert_and_fetch(auth_client):
    # 1. Insert Data
    # Note: Adjust the payload and URL according to your implementation
    insert_url = f"/{app.lower()}/{name}/insert/"
    
    payload = {{
        "run_id": "test_auto_run",
        "rows": [{{}}] # Add dummy data matching your serializer
    }}
    
    response = auth_client.post(insert_url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    # 2. Fetch Data
    fetch_url = f"/{app.lower()}/{name}/fetch/"
    response = auth_client.get(fetch_url, {{"run_id": "test_auto_run"}})
    assert response.status_code == status.HTTP_200_OK
"""