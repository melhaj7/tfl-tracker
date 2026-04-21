import requests

BASE_URL = "https://api.tfl.gov.uk"
TIMEOUT = 10 # Seconds to wait before giving up

session = requests.Session()

def _make_request(path, app_key, params=None):
    url = f"{BASE_URL}{path}"
    
    # Merge app_key into whatever other params we have
    query_params = {"app_key": app_key}
    if params:
        query_params.update(params)

    response = session.get(url, params=query_params, timeout=TIMEOUT)
    response.raise_for_status() 
    return response.json()

def fetch_all_lines(app_key, modes):
    all_lines = []
    for mode in modes:
        data = _make_request(f"/Line/Mode/{mode}", app_key)
        if data:
            all_lines.extend([line["id"] for line in data])
    return all_lines

def fetch_arrivals(app_key, line_id):
    return _make_request(f"/Line/{line_id}/Arrivals", app_key)

def fetch_disruptions(app_key, line_id):
    return _make_request(f"/Line/{line_id}/Disruption", app_key)

def fetch_stop_points(app_key, line_id):
    return _make_request(f"/Line/{line_id}/StopPoints", app_key)

def fetch_timetable(app_key, line_id, stop_naptan_id, direction):
    return _make_request(f"/Line/{line_id}/Timetable/{stop_naptan_id}", app_key, {"direction": direction})
