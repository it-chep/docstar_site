from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render


class CustomErrorHandlerMiddleware:
    def process_exception(self, request, exception):
        return HttpResponse('docstar/500.html')

