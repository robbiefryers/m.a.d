from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets

from django.contrib.auth.models import User, Group 
from models import Categories, Activities, act_day
from MAD.serializers import CategorySerializer, GroupSerializer, ActivitySerializer

from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        print 'log in request received'


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def activity_list(request):

    acts = Activities.objects.all()
    serializer = ActivitySerializer(acts, many=True)
    print "Get request processed"
    return JSONResponse(serializer.data)


@csrf_exempt
def category_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cats = Categories.objects.all()
        serializer = CategorySerializer(cats, many=True)
        print "Get request processed"
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def category_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        cat = Categories.objects.get(pk=pk)
    except Categories.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(cat)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(cat, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        cat.delete()
        return HttpResponse(status=204)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
