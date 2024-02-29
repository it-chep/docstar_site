import json
import os

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_request(request):
    login = os.getenv("CDEK_LOGIN")
    secret = os.getenv("CDEK_PASSWORD")
    base_url = os.getenv("CDEK_URL")

    if request.method == 'GET':
        get_data = request.GET.dict()
    elif request.method == 'POST':
        get_data = request.POST.dict()
    else:
        get_data = {}

    body = request.body.decode('utf-8')
    body_data = json.loads(body) if body else {}

    request_data = {**get_data, **body_data}

    if 'action' not in request_data:
        return JsonResponse({'message': 'Action is required'}, status=400)

    auth_token = get_auth_token(login, secret)

    action = request_data['action']
    if action == 'offices':
        response = get_offices(auth_token, request_data, base_url)
    elif action == 'calculate':
        response = calculate(auth_token, request_data, base_url)
    else:
        return JsonResponse({'message': 'Unknown action'}, status=400)

    return JsonResponse(response)


def get_auth_token(login, secret):
    token_url = f'{os.getenv("CDEK_URL")}' + '/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': login,
        'client_secret': secret,
    }
    response = requests.post(token_url, data=data)
    response_json = response.json()
    if 'access_token' not in response_json:
        raise RuntimeError('Server not authorized to CDEK API')
    return response_json['access_token']


def get_offices(auth_token, request_data, base_url):
    url = f'{base_url}/deliverypoints'
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json',
    }
    response = requests.get(url, params=request_data, headers=headers)
    return response.json()


def calculate(auth_token, request_data, base_url):
    url = f'{base_url}/calculator/tarifflist'
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json',
    }
    response = requests.post(url, json=request_data, headers=headers)
    return response.json()
