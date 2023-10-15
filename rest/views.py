from django.shortcuts import render
from rest_framework import viewsets
from rest.models import Company
from rest.serializers import CompanySerializer
from rest.forms import CSVUploadForm
from django.contrib import messages
import csv
from datetime import datetime
from io import TextIOWrapper
from decimal import Decimal
# from django.utils.text import unescape

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'Please select a CSV file.')
            else:
                try:
                    csv_data = TextIOWrapper(csv_file, encoding='utf-8')
                    data = csv.reader(csv_data, delimiter=',')
                    # print(len(data))
                    next(data)
                except UnicodeDecodeError:
                    csv_data = TextIOWrapper(csv_file, encoding='iso-8859-1')
                    data = csv.reader(csv_data, delimiter=',')
                    next(data)

            for row in data:
                    try:
                        CASE_SUBMITTED = datetime.strptime(row[2], "%d-%m-%Y").date()
                        DECISION_DATE = datetime.strptime(row[3], "%d-%m-%Y").date()
                        ORIGINAL_CERT_DATE = datetime.strptime(row[39], "%d-%m-%Y").date()
                        VISA_CLASS = row[4]
                        EMPLOYMENT_START_DATE =  datetime.strptime(row[5], "%d-%m-%Y").date()
                        EMPLOYMENT_END_DATE =  datetime.strptime(row[6], "%d-%m-%Y").date()
                        SOC_CODE = row[20]
                        PREVAILING_WAGE = Decimal(row[25].replace(',', ''))
                        WAGE_RATE_OF_PAY_FROM = Decimal(row[30].replace(',',''))
                        WAGE_RATE_OF_PAY_TO = Decimal(row[31].replace(',',''))


                    except ValueError:
                        messages.error(request, 'Invalid date format in CSV. Please use DD-MM-YYYY format.')
                        return render(request, 'upload_csv.html', {'form': form})

                    Company.objects.create(
                    CASE_NUMBER = row[0],
                    CASE_STATUS = row[1],
                    CASE_SUBMITTED = CASE_SUBMITTED,
                    DECISION_DATE = DECISION_DATE,
                    VISA_CLASS = VISA_CLASS,
                    EMPLOYMENT_START_DATE = EMPLOYMENT_START_DATE,
                    EMPLOYMENT_END_DATE = EMPLOYMENT_END_DATE,
                    EMPLOYER_NAME = row[7],
                    EMPLOYER_ADDRESS = row[8],
                    EMPLOYER_CITY = row[9],
                    EMPLOYER_STATE = row[10],
                    EMPLOYER_POSTAL_CODE = row[11],
                    EMPLOYER_COUNTRY = row[12],
                    EMPLOYER_PROVINCE = row[13],
                    EMPLOYER_PHONE = row[14],
                    EMPLOYER_PHONE_EXT = row[15],
                    AGENT_ATTORNEY_NAME = row[16],
                    AGENT_ATTORNEY_CITY = row[17],
                    AGENT_ATTORNEY_STATE = row[18],
                    JOB_TITLE = row[19],
                    SOC_CODE = SOC_CODE,
                    SOC_NAME = row[21],
                    NAIC_CODE = row[22],
                    TOTAL_WORKERS = row[23],
                    FULL_TIME_POSITION = row[24],
                    PREVAILING_WAGE = PREVAILING_WAGE,
                    PW_UNIT_OF_PAY = row[26],
                    PW_WAGE_SOURCE = row[27],
                    PW_SOURCE_YEAR = row[28],
                    PW_SOURCE_OTHER = row[29],
                    WAGE_RATE_OF_PAY_FROM = WAGE_RATE_OF_PAY_FROM,
                    WAGE_RATE_OF_PAY_TO = WAGE_RATE_OF_PAY_TO,
                    WAGE_UNIT_OF_PAY = row[32],
                    HB = row[33],
                    WILLFUL_VIOLATOR = row[34],
                    WORKSITE_CITY = row[35],
                    WORKSITE_COUNTY = row[36],
                    WORKSITE_STATE = row[37],
                    WORKSITE_POSTAL_CODE = row[38],
                    ORIGINAL_CERT_DATE = ORIGINAL_CERT_DATE
                )

                    messages.success(request, 'CSV data has been uploaded and saved to the database.')

    else:
        form = CSVUploadForm()
 
    # print(Company.objects.all())
    return render(request, 'upload_csv.html',{'form': form})


from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def count_records(request):
    total_unique_case_numbers = Company.objects.values('CASE_NUMBER').count()
    # print(Company.objects.all())
    return Response({'total_records': total_unique_case_numbers})



from django.db.models import Avg

@api_view(['GET'])
def mean_salary(request):
    mean_salary = Company.objects.aggregate(Avg('PREVAILING_WAGE'))['PREVAILING_WAGE__avg']
    return Response({'mean_salary': mean_salary})



@api_view(['GET'])
def median_salary(request):
    total_records = Company.objects.count()
    median_salary = Company.objects.order_by('PREVAILING_WAGE')[total_records // 2]
    return Response({'median_salary': median_salary.PREVAILING_WAGE})

@api_view(['GET'])
def percentile_25(request):
    total_records = Company.objects.count()
    percentile_25 = Company.objects.order_by('PREVAILING_WAGE')[total_records // 4]
    return Response({'percentile_25_salary': percentile_25.PREVAILING_WAGE})

@api_view(['GET'])
def percentile_75(request):
    total_records = Company.objects.count()
    percentile_75 = Company.objects.order_by('PREVAILING_WAGE')[3 * (total_records // 4)]
    return Response({'percentile_75_salary': percentile_75.PREVAILING_WAGE})