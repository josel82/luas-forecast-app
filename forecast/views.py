from django.shortcuts import render
from django.http import Http404, JsonResponse
import requests
from .utils import STOPS, format_response, generateURL




def get_luas_times(request):
    stop_id = request.GET.get("stop", "stillorgan")
    try:
        resp = requests.get(generateURL(stop_id), timeout=10)
        resp.raise_for_status()
    except:
        raise Http404()
    arrivals = format_response(resp)
    return render(request, "forecast/index.html", {
        "arrivals": arrivals,
        "stops": STOPS,
        "current_stop": stop_id,
        })

def luas_times_json(request, stop_id):
    try:
        resp = requests.get(generateURL(stop_id), timeout=10)
        resp.raise_for_status()
    except:
        return JsonResponse({"error": "Failed to fetch data"}, status=500)
    
    arrivals = format_response(resp)
    return JsonResponse({
        "arrivals": arrivals,
        })