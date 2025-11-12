from datetime import datetime
from django.utils import timezone
import xmltodict


stop_list = [
    {"id": "abb", "name": "Abbey Street"},
    {"id": "bal", "name": "Balally"},
    {"id": "baw", "name": "Ballyogan Wood"},
    {"id": "bee", "name": "Beechwood"},
    {"id": "bel", "name": "Belgard"},
    {"id": "bla", "name": "Blackhorse"},
    {"id": "blu", "name": "Bluebell"},
    {"id": "bre", "name": "Brennanstown"},
    {"id": "brd", "name": "Broadstone - University"},
    {"id": "bro", "name": "Broombridge"},
    {"id": "bri", "name": "Brides Glen"},
    {"id": "bus", "name": "Busáras"},
    {"id": "cab", "name": "Cabra"},
    {"id": "cck", "name": "Carrickmines"},
    {"id": "cha", "name": "Charlemont"},
    {"id": "che", "name": "Cherrywood"},
    {"id": "cvn", "name": "Cheeverstown"},
    {"id": "cit", "name": "Citywest Campus"},
    {"id": "con", "name": "Connolly"},
    {"id": "coo", "name": "Cookstown"},
    {"id": "cow", "name": "Cowper"},
    {"id": "cpk", "name": "Central Park"},
    {"id": "daw", "name": "Dawson"},
    {"id": "dep", "name": "Depot"},
    {"id": "dom", "name": "Dominick"},
    {"id": "dri", "name": "Drimnagh"},
    {"id": "dun", "name": "Dundrum"},
    {"id": "fat", "name": "Fatima"},
    {"id": "fet", "name": "Fettercairn"},
    {"id": "for", "name": "Fortunestown"},
    {"id": "fou", "name": "Four Courts"},
    {"id": "gal", "name": "The Gallops"},
    {"id": "gdk", "name": "George's Dock"},
    {"id": "gle", "name": "Glencairn"},
    {"id": "gol", "name": "Goldenbridge"},
    {"id": "gra", "name": "Grangegorman"},
    {"id": "har", "name": "Harcourt"},
    {"id": "heu", "name": "Heuston"},
    {"id": "hos", "name": "Hospital"},
    {"id": "jam", "name": "James's"},
    {"id": "jer", "name": "Jervis"},
    {"id": "kil", "name": "Kilmacud"},
    {"id": "kin", "name": "Kingswood"},
    {"id": "kyl", "name": "Kylemore"},
    {"id": "lau", "name": "Laughanstown"},
    {"id": "leo", "name": "Leopardstown Valley"},
    {"id": "mar", "name": "Marlborough"},
    {"id": "mys", "name": "Mayor Square - NCI"},
    {"id": "mil", "name": "Milltown"},
    {"id": "mus", "name": "Museum"},
    {"id": "ogp", "name": "O'Connell - GPO"},
    {"id": "oup", "name": "O'Connell - Upper"},
    {"id": "par", "name": "Parnell"},
    {"id": "phi", "name": "Phibsborough"},
    {"id": "rcc", "name": "Racecourse"},
    {"id": "ran", "name": "Ranelagh"},
    {"id": "red", "name": "Red Cow"},
    {"id": "ria", "name": "Rialto"},
    {"id": "sag", "name": "Saggart"},
    {"id": "sam", "name": "Sandyford"},
    {"id": "sdk", "name": "Spencer Dock"},
    {"id": "smi", "name": "Smithfield"},
    {"id": "sti", "name": "Stillorgan"},
    {"id": "sts", "name": "St. Stephen's Green"},
    {"id": "sui", "name": "Suir Road"},
    {"id": "tal", "name": "Tallaght"},
    {"id": "tpt", "name": "The Point"},
    {"id": "try", "name": "Trinity"},
    {"id": "wes", "name": "Westmoreland"},
    {"id": "win", "name": "Windy Arbour"},
]

STOPS = sorted(stop_list, key=lambda s: s["name"].lower())


def generateURL(stop_id):
    return f"http://luasforecasts.rpa.ie/xml/get.ashx?action=forecast&stop={stop_id}&encrypt=false"


def format_response(resp):
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