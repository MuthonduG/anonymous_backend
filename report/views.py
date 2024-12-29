from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Report
from .serializers import UserReportSerializer
import logging

logger = logging.getLogger(__name__)
# Create your views here.

# get all reports
@api_view(['GET'])
def getReports(request):
    reports = Report.objects.all()
    serializer = UserReportSerializer(reports, many=True)
    return Response(serializer.data)

# get a specific report
@api_view(['GET'])
def getReport(request, pk):
    report = get_object_or_404(Report, id=pk)
    serializer = UserReportSerializer(report, many=False)
    return Response(serializer.data)

# make a report
@api_view(['POST'])
def createReport(request):
    serializer = UserReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.error(f"Report creation errors: {serializer.errors}")
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# update an existing report
@api_view(['PUT'])
def updateReport(request, pk):
    report = get_object_or_404(Report, id=pk)
    serializer = UserReportSerializer(instance=report, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

# delete an existing report
@api_view(['DELETE'])
def deleteReport(request, pk):
    report = get_object_or_404(Report, id=pk)
    report.delete()
    return Response(
        {"message": "Report successfully deleted!"},
        status=status.HTTP_204_NO_CONTENT
    )
