
from googlemaps import convert
import googlemaps



def distanceBetween( origins, destinations,
                    mode="driving", language=None, avoid=None, units=None,
                    departure_time=None, arrival_time=None, transit_mode=None,
                    transit_routing_preference=None, traffic_model=None, region=None):
   

    params = {
        "origins": convert.location_list(origins),
        "destinations": convert.location_list(destinations)
    }

    if mode:
        # NOTE(broady): the mode parameter is not validated by the Maps API
        # server. Check here to prevent silent failures.
        if mode not in ["driving", "walking", "bicycling", "transit"]:
            raise ValueError("Invalid travel mode.")
        params["mode"] = mode

    if language:
        params["language"] = language

    if avoid:
        if avoid not in ["tolls", "highways", "ferries"]:
            raise ValueError("Invalid route restriction.")
        params["avoid"] = avoid

    if units:
        params["units"] = units

    if departure_time:
        params["departure_time"] = convert.time(departure_time)

    if arrival_time:
        params["arrival_time"] = convert.time(arrival_time)

    if departure_time and arrival_time:
        raise ValueError("Should not specify both departure_time and"
                         "arrival_time.")

    if transit_mode:
        params["transit_mode"] = convert.join_list("|", transit_mode)

    if transit_routing_preference:
        params["transit_routing_preference"] = transit_routing_preference

    if traffic_model:
        params["traffic_model"] = traffic_model

    if region:
        params["region"] = region
    client = googlemaps.Client(key='AIzaSyDeDdChsSQWwTVeIKLP0CvPDG6Z_VRKaRg')
    response = client._request("/maps/api/distancematrix/json", params)
    
    if response.get("status") != 'OK':
        print(response)
        return response
    else:
        rows = response.get("rows")
        elements =rows[0].get("elements")
        text_distance = elements[0].get("distance").get("text")
        duration_text = elements[0].get("duration").get("text")

        valuableData = f'The distance between {origins} and {destinations} is {text_distance} and it will take you about {duration_text} to reach {destinations} by {mode}' 

        print(valuableData)
        return valuableData


# print(distanceBetween("96 symonds street auckland 1010","mt albert primary auckland"))