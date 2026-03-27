from ..models.sample_data import SampleData

def insert_sample_data(rows, run_id):
    for row in rows:
        SampleData.objects.create(run_id=run_id)
    if not rows:
        SampleData.objects.create(run_id=run_id)

def fetch_sample_data(run_id=None):
    qs = SampleData.objects.all()
    if run_id:
        qs = qs.filter(run_id=run_id)
    return [{"run_id": obj.run_id, "dummy_val": "data"} for obj in qs]
