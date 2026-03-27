from django.db import models


class SampleData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    run_id = models.CharField(max_length=50)

    class Meta:
        db_table = "sample_data"

