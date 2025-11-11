from datetime import datetime
from django.utils import timezone
import xmltodict


STOPS = [
    {"id": "hin", "name": "Heuston"},
    {"id": "hct", "name": "Heuston"},
    {"id": "tpt", "name": "The Point"},
    {"id": "sdk", "name": "Spencer Dock"},
    {"id": "mys", "name": "Mayor Square - NCI"},
    {"id": "gdk", "name": "George's Dock"},
    {"id": "con", "name": "Connolly"},
    {"id": "bus", "name": "Busáras"},
    {"id": "abb", "name": "Abbey Street"},
    {"id": "jer", "name": "Jervis"},
    {"id": "fou", "name": "Four Courts"},
    {"id": "smi", "name": "Smithfield"},
    {"id": "mus", "name": "Museum"},
    {"id": "heu", "name": "Heuston"},
    {"id": "jam", "name": "James's"},
    {"id": "fat", "name": "Fatima"},
    {"id": "ria", "name": "Rialto"},
    {"id": "sui", "name": "Suir Road"},
    {"id": "gol", "name": "Goldenbridge"},
    {"id": "dri", "name": "Drimnagh"},
    {"id": "bla", "name": "Blackhorse"},
    {"id": "blu", "name": "Bluebell"},
    {"id": "kyl", "name": "Kylemore"},
    {"id": "red", "name": "Red Cow"},
    {"id": "kin", "name": "Kingswood"},
    {"id": "bel", "name": "Belgard"},
    {"id": "coo", "name": "Cookstown"},
    {"id": "hos", "name": "Hospital"},
    {"id": "tal", "name": "Tallaght"},
    {"id": "fet", "name": "Fettercairn"},
    {"id": "cvn", "name": "Cheeverstown"},
    {"id": "cit", "name": "Citywest Campus"},
    {"id": "for", "name": "Fortunestown"},
    {"id": "sag", "name": "Saggart"},
    {"id": "dep", "name": "Depot"},
    {"id": "stx", "name": "St. Stephen's Green"},
    {"id": "bro", "name": "Broombridge"},
    {"id": "cab", "name": "Cabra"},
    {"id": "phi", "name": "Phibsborough"},
    {"id": "gra", "name": "Grangegorman"},
    {"id": "brd", "name": "Broadstone - University"},
    {"id": "dom", "name": "Dominick"},
    {"id": "par", "name": "Parnell"},
    {"id": "oup", "name": "O'Connell - Upper"},
    {"id": "ogp", "name": "O'Connell - GPO"},
    {"id": "mar", "name": "Marlborough"},
    {"id": "wes", "name": "Westmoreland"},
    {"id": "try", "name": "Trinity"},
    {"id": "daw", "name": "Dawson"},
    {"id": "sts", "name": "St. Stephen's Green"},
    {"id": "har", "name": "Harcourt"},
    {"id": "cha", "name": "Charlemont"},
    {"id": "ran", "name": "Ranelagh"},
    {"id": "bee", "name": "Beechwood"},
    {"id": "cow", "name": "Cowper"},
    {"id": "mil", "name": "Milltown"},
    {"id": "win", "name": "Windy Arbour"},
    {"id": "dun", "name": "Dundrum"},
    {"id": "bal", "name": "Balally"},
    {"id": "kil", "name": "Kilmacud"},
    {"id": "sti", "name": "Stillorgan"},
    {"id": "sam", "name": "Sandyford"},
    {"id": "cpk", "name": "Central Park"},
    {"id": "gle", "name": "Glencairn"},
    {"id": "gal", "name": "The Gallops"},
    {"id": "leo", "name": "Leopardstown Valley"},
    {"id": "baw", "name": "Ballyogan Wood"},
    {"id": "rcc", "name": "Racecourse"},
    {"id": "cck", "name": "Carrickmines"},
    {"id": "bre", "name": "Brennanstown"},
    {"id": "lau", "name": "Laughanstown"},
    {"id": "che", "name": "Cherrywood"},
    {"id": "bri", "name": "Brides Glen"},
]



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