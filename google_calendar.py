from datetime import datetime

def get_calendar_events():

    """
    REAL VERSION (requires OAuth setup)

    For now returns structure ready for Google API
    """

    return [
        {
            "title": "Chinese New Year",
            "start": "2027-02-06",
            "end": "2027-02-08",
            "crowd": 500000
        },
        {
            "title": "Hajj Season Travel Peak",
            "start": "2027-06-01",
            "end": "2027-06-10",
            "crowd": 1000000
        }
    ]


def event_risk(event):

    title = event["title"].lower()

    if "hajj" in title:
        return 1.5
    if "new year" in title:
        return 1.3

    return 1.1