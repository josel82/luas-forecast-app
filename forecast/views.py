from django.shortcuts import render
from django.http import Http404, JsonResponse
from datetime import datetime
from django.utils import timezone
import requests
import xmltodict

# Only for Windy Arbour Stop PID: win
LUAS_URL = "http://luasforecasts.rpa.ie/xml/get.ashx?action=forecast&stop=win&encrypt=false"

def helper(resp):
    # Parse XML to Python dict
    xd = xmltodict.parse(resp.text)

    # The exact structure can vary; inspect top-level keys:
    # print(xd.keys())
    # Typical path: xd['stopInfo']['direction'][...]['tram']
    stop_info = xd.get('stopInfo', {})
    directions = stop_info.get('direction', [])
    if isinstance(directions, dict):
        directions = [directions]

    arrivals = []
    for d in directions:
        dir_name = d.get('@name') or d.get('directionName') or 'unknown'
        trams = d.get('tram', [])
        if isinstance(trams, dict):
            trams = [trams]
        for t in trams:
            minutes = t.get('@dueMins') or t.get('dueMins') or t.get('expMin')
            arrivals.append({
                'direction': dir_name,
                'destination': t.get('@destination') or t.get('destination'),
                'due_mins': int(minutes) if minutes and minutes.isdigit() else minutes,
                'timestamp': timezone.localtime(timezone.now())
            })

    # Show next arrivals
    arrivals = sorted(arrivals, key=lambda x: x['due_mins'] if isinstance(x['due_mins'], int) else 9999)
    return arrivals


def get_luas_times(request):

    try:
        resp = requests.get(LUAS_URL, timeout=10)
        resp.raise_for_status()
    except:
        raise Http404()
    arrivals = helper(resp)
    return render(request, "forecast/index.html", {"arrivals": arrivals})

def luas_times_json(request):
    try:
        resp = requests.get(LUAS_URL, timeout=10)
        resp.raise_for_status()
    except:
        return JsonResponse({"error": "Failed to fetch data"}, status=500)
    
    arrivals = helper(resp)
    return JsonResponse({"arrivals": arrivals})