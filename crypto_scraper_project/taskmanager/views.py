from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import scrape_coins
from .models import ScrapingJob
import uuid

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get("coins", [])
        if not coins:
            return Response({"error": "No coins provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        job_id = uuid.uuid4()
        for coin in coins:
            scrape_coins.delay(job_id, coin)
        
        ScrapingJob.objects.create(id=job_id)
        return Response({"job_id": job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapingJob.objects.get(id=job_id)
        except ScrapingJob.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "job_id": job_id,
            "tasks": job.get_results()
        })
