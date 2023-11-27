"""
URL configuration for Codemonk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Intern.views import *
from Intern import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view=get_swagger_view(title=" API Documentation")
urlpatterns = [
    path('get_books/',get_books),
    path('api_documentation/', schema_view),
    path('get_all_books/',get_all_books),
    path('book_list/',views.BookList.as_view()),
    # path('mypagination/',views.MyPagination.as_view()),
    path('update_book/',update_book),
    path('delete_book/',delete_book),
    path('post_books/',post_books),
    path('book_detail/',book_detail),
    # path('',student_home),
    path('admin/', admin.site.urls),
    # path('verify-email/', verify_email, name='verify_email'),
]
if settings.DEBUG:
    urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)