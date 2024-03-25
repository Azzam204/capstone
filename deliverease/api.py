from secret import *


params = {
    'key': api_key,
    'fields' : '*'
}

url = 'https://routes.googleapis.com/directions/v2:computeRoutes'


def create_data(arr):
    data = {
        'origin' : {
            'via' : 'false',
            'vehicleStopover' : 'false',
            'sideOfRoad' : 'false',
            'address' :'61 Malcolm X Blvd, New York, NY 10026'
        },
        'destination' : {
            'via' : 'false',
            'vehicleStopover' : 'false',
            'sideOfRoad' : 'false',
            'address' :'3279 Westchester Ave, Bronx, NY 10461'
        },
        'intermediates' : [
            {
                'via' : 'false',
                'vehicleStopover' : 'false',
                'sideOfRoad' : 'false',
                'address' : address
            }
            for address in arr
        ],
        'optimizeWaypointOrder' : 'true',
        'routingPreference' : 'TRAFFIC_AWARE'
    }

    return data
