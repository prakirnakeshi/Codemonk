import io
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from Intern import serializer
from Intern.pagination import MyPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from Intern.pagination import *
from rest_framework.filters import OrderingFilter
from Intern.serializer import BookSeralizer



from Intern.models import *

#If we want to send data from frontend to backend
@api_view(['POST'])
def post_books(request):
    response ={'status': 200}
    data=request.data # fro sending data from frontenc to database
    serializer=BookSeralizer(data=data)
    if serializer.is_valid(): #if the data will be valid, then only will save.
        serializer.save()
        return Response(response)
    return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk=None):
    if pk is None:
        # Handle the case where no primary key is provided (e.g., list all students)
        books = Book.objects.all()
        serializer = BookSeralizer(books, many=True)
        return Response(serializer.data)

    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSeralizer(book)
        return Response(serializer.data)
    # Handle other HTTP methods (PUT, DELETE) as needed

    # Update an existing book
    elif request.method == 'PUT':
        serializer = BookSeralizer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'book updated successfully'})
        return Response(serializer.errors)

    # Delete an existing book
    elif request.method == 'DELETE':
        book.delete()
        return Response(serializer.errors)
    
    



@api_view(['GET','POST'])
def get_home(request):
    response ={'status': 200, 'message':'Hello from res'}
    if request.method == 'POST':
        print('POST')
    else:
        print('GET')
    return Response(response)
@api_view()
def home(request):
    response ={'status': 200, 'message':'Hello from res'}
    return Response(response)


# def student_home(request):
#     stu=Student.objects.get(age=2) # model object
#     serializer=BookSeralizer(stu) #Converted to python data type from complex data type
#     json_data= JSONRenderer().renderer(serializer.data) # Python data -> JSON data  now it can be can be returned to API
#     return HttpResponse(json_data, content_type='application/json')



@api_view(['GET'])
def get_all_books(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSeralizer(books, many=True)
        return Response({'status': 'All books retrieved successfully', 'data': serializer.data})

@api_view(['GET','POST'])
def get_books(request):
    if(request.method=="GET"):
        json_data=request.body
        stream=io.BytesIO(json_data) 
        python_data=JSONParser().parse(stream)
        id=python_data.get('id')
        if id is not None:
            try:
                book = Book.objects.get(id=id)
                serializer = BookSeralizer(book)
                json_data = JSONRenderer().render(serializer.data)
                # Instead of returning JSON data, use DRF Response
                return Response({'status': 'book retrieved successfully', 'data': serializer.data})
            except Book.DoesNotExist:
                return Response({'status': 'Student not found'}, status=404)
        return Response({'status': 'Invalid request. Please provide an "id" parameter.'}, status=400)       
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

        serializer = BookSeralizer(data=python_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'book created successfully', 'data': serializer.data}, status=201)
        else:
            return Response({'status': 'Invalid data', 'errors': serializer.errors}, status=400)
    return Response({'status': 'Invalid request. Use a POST method.'}, status=400)

@api_view(['PUT'])
def update_book(request):
    json_data=request.body
    stream=io.BytesIO(json_data) 
    python_data=JSONParser().parse(stream)
    id=python_data.get('id')
    if id is not None:
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({'status': 'Book not found'}, status=404)
        if request.method == "PUT":
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)

            serializer = BookSeralizer(book, data=python_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'Student updated successfully', 'data': serializer.data})
            return Response({'status': 'Invalid data provided', 'errors': serializer.errors}, status=400)

@api_view(['DELETE'])
def delete_book(request):
    json_data = request.body
    stream = io.BytesIO(json_data)
    python_data = JSONParser().parse(stream)
    id = python_data.get('id')

    if id is not None:
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({'status': 'book not found'}, status=404)

        if request.method == "DELETE":
            book.delete()
            return Response({'status': 'book deleted successfully'})
    
    return Response({'status': 'Bad Request. Please provide a valid "id" parameter in the request body.'}, status=400)



#FILTERING
class BookList(ListAPIView):
    queryset=Book.objects.all()
    serializer_class = BookSeralizer
    filter_backends = [DjangoFilterBackend] #this is to be written in each view class in which we want to use the filter
    filterset_fields=['name','age']
    pagination_class=MyPagination # class for custom record to be displayed per page