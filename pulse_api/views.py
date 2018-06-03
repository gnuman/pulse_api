import csv
import io
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from .models import Pulse
from .serializers import PulseSerializer

# Create your views here.
PULSE_TYPE = 'pulse'

def get_serializer(queryset, many=True):
    return PulseSerializer(
        queryset,
        many=many,
    )

def pulse_requst_parser(data):
    '''
        This function parses the requst from client
        We expect data to be in following format
        "data": {
            "type": "pulse",
            "attributes": {
                ....
            }
        }
        This function checks if data type is pulse 
        If we find data type is not pulse or request don't have reqd arguments then it returns empty dict
        So that it will fail in next step
    '''

    data_type = data['data'].get('type') if data.get('data', {}) else '' 
    if data_type == PULSE_TYPE:
        return data['data'].get('attributes', {})
    return {}

def pulse_resp_for_dict(data):
    ''' 
        JSON standard expects id as seperate attr
        TODO now I do data mutation which is not good, need to fix it
        I could write generic pulse_response, which would accept data as type
        But that function will return either dict type or list type
        I prefer consistant return type
    '''
    return { 
        "data": {
            "type": PULSE_TYPE,
            "id": data.pop("id"),
            "attributes": data,
        }
    }
    

def pulse_resp_for_list(data):
    return [
        {
            "data": {
                "type": PULSE_TYPE,
                "id": item.pop("id"),
                "attributes": item,
            }
        }
        for item in data 
    ]
    

@api_view(['GET', 'POST'])
def pulse_bulk_operation(request):
    """
    List all pulses or create a new
    curl -i -X POST -H "Content-Type: application/json" -d '  {"name": "my pulse", "maximum_rabi_rate": 100.32, "polar_angle": 0.1, "pulse_type": "cinbb" }' http://127.0.0.1:3200/pulses/
    """
    if request.method == 'GET':
        pulse_objects = Pulse.objects.filter(deleted=False)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(pulse_objects, request)
        serializer = PulseSerializer(result_page, many=True)
        return paginator.get_paginated_response(pulse_resp_for_list(serializer.data))

    elif request.method == 'POST':
        data = pulse_requst_parser(request.data)
        serializer = PulseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(pulse_resp_for_dict(serializer.data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pulse_single_operation(request, id):
    """
    Get update or Delete existing Pulse
     curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://127.0.0.1:3200/pulses/1/
     curl -X PUT -H "Content-Type: application/json" -d '{"name":"Foo bar", "pulse_type": "corp", "maximum_rabi_rate": 10.3, "polar_angle": 1.0}' http://127.0.0.1:3200/pulses/1/
     curl -X "DELETE" http://127.0.0.1:3200/pulses/1/
    """
    try:
        pulse = Pulse.objects.get(id=id, deleted=False)
    except Pulse.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PulseSerializer(pulse)
        return Response(pulse_resp_for_dict(serializer.data), status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PulseSerializer(pulse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(pulse_resp_for_dict(serializer.data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pulse.deleted = True
        pulse.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def pulse_download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    serializer = get_serializer(
        Pulse.objects.filter(deleted=False),
        many=True
    )

    header = PulseSerializer.Meta.fields

    writer = csv.DictWriter(response, fieldnames=header)
    writer.writerows(serializer.data)
    
    return response

@api_view(['PATCH', 'POST'])
@parser_classes((MultiPartParser,))
def pulse_upload(request, format=None):
    csv_file = request.data.get('csv')
    csv_data = csv_file.read().decode('utf-8')
    io_string = io.StringIO(csv_data)
    reader = csv.reader(io_string, delimiter=',', quotechar='"')
    skip_header = next(reader)
    data = [
        {
            'name': row[0],
            'pulse_type': row[1],
            'maximum_rabi_rate': row[2],
            'polar_angle': row[3]
        }
        for row in reader
    ]
    serializer = PulseSerializer(data=data, many=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(pulse_resp_for_list(serializer.data), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)