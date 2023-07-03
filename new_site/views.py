from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'docstar/404.html', status=404, )


def server_not_found_view(request, exception):
    return render(request, 'docstar/404.html', status=404, )
