import uuid
from django.db import models

class ScrapingJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    results = models.JSONField(default=list)

    def get_results(self):
        return self.results
