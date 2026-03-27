from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..services.sample_result_service import insert_sample_result, fetch_sample_result
from ..serializers.sample_result_serializer import SampleResultSerializer


# -------- INSERT --------
@api_view(["POST"])
def insert_sample_result_api(request):
    serializer = SampleResultSerializer(
        data=request.data.get("rows", []), many=True
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    insert_sample_result(
        rows=serializer.validated_data,
        run_id=request.data.get("run_id")
    )

    return Response({"status": "success"})


# -------- FETCH --------
@api_view(["GET"])
def fetch_sample_result_api(request):
    run_id = request.GET.get("run_id")

    data = fetch_sample_result(run_id=run_id)

    serializer = SampleResultSerializer(data, many=True)

    return Response(serializer.data)
