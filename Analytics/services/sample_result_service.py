from ..models.sample_result import SampleResult

def insert_sample_result(rows, run_id):
    for row in rows:
        SampleResult.objects.create(run_id=run_id)
    if not rows:
        SampleResult.objects.create(run_id=run_id)

def fetch_sample_result(run_id=None):
    qs = SampleResult.objects.all()
    if run_id:
        qs = qs.filter(run_id=run_id)
    return [{"run_id": obj.run_id, "dummy_val": "data"} for obj in qs]
