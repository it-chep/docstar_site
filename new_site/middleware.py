from django.http import HttpResponse


class CustomErrorHandlerMiddleware:
    def process_exception(self, request, exception):
        return HttpResponse('docstar/500.html')

