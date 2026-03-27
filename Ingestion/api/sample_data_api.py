from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..services.sample_data_service import insert_sample_data, fetch_sample_data
from ..serializers.sample_data_serializer import SampleDataSerializer


# -------- INSERT --------
@api_view(["POST"])
def insert_sample_data_api(request):
    serializer = SampleDataSerializer(
        data=request.data.get("rows", []), many=True
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    insert_sample_data(
        rows=serializer.validated_data,
        run_id=request.data.get("run_id")
    )

    return Response({"status": "success"})


# -------- FETCH --------
@api_view(["GET"])
def fetch_sample_data_api(request):
    run_id = request.GET.get("run_id")

    data = fetch_sample_data(run_id=run_id)

    serializer = SampleDataSerializer(data, many=True)

    return Response(serializer.data)
