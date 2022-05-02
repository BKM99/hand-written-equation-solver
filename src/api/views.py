from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import json
from .utils import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def home_view(request):
    return HttpResponse("default api view (base)")


@api_view(['POST', 'GET'])
def data_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)['imageData']
            data_decoded = decode_base64_to_arr(data)
            result = solve(data_decoded)
            post_data = {'result': result}
            return JsonResponse(post_data)
        except:
            return JsonResponse({'result': 'error during calculation, please try again.'})


    return HttpResponse("data goes here")
