"""Module providing a driver for the Distance and algorithm comparisions."""
# Import math LibraryB
import math
import dictBuilder

FILENAME = "49Cities.csv"
RADIUS = 3958.8
DEG_TO_RAD = math.pi/180

def distance_between_cities(city_a, city_b):
    """Distance between two cites function."""
    lat_a = float(city_a['lat'])
    lat_b = float(city_b['lat'])
    long_a = float(city_a['long'])
    long_b = float(city_b['long'])
    return ((2 * RADIUS) * (math.asin(math.sqrt(.5 - (math.cos((lat_a - lat_b) * DEG_TO_RAD)/2)
        + math.cos(lat_b*DEG_TO_RAD) * math.cos(lat_a*DEG_TO_RAD) * (1-(math.cos((long_a - long_b)
        * DEG_TO_RAD))) /2))))

def nearest_neighbor(city_a, cities_dictionary,
    unchecked_cities_dictionary=None, routes=None, route_distance=0):
    """Nearest Neighbor Algoritm."""
    # print(cities_dictionary)
    if unchecked_cities_dictionary is None:
        unchecked_cities_dictionary = cities_dictionary.copy()
    unchecked_cities_dictionary.pop(city_a['name'])
    if len(unchecked_cities_dictionary) == 0:
        # print(city_a, " | ", cities_dictionary[routes[0]], " | ", routes [0])
        route_distance += distance_between_cities(city_a, cities_dictionary[routes[0]])
        return {'startingCity':routes[0],'routes':routes, 'route_distance': route_distance}
    if routes is None:
        routes = [city_a['name']]
    nearest_city = None
    for next_city, next_data in unchecked_cities_dictionary.items():
        if next_city != city_a['name']:
            distance = distance_between_cities(city_a, next_data)
            if nearest_city is None:
                nearest_city = {'name':next_city, 'distance':distance}
            else:
                if distance < nearest_city['distance']:
                    nearest_city = {'name':next_city, 'distance':distance}
    if nearest_city is None:
        # print(unchecked_cities_dictionary)
        print("Error in the program: no nearest_city")
        return {'startingCity':routes[0],'routes ':routes,
            'route_distance': route_distance, 'error': "Did not finish"}
    routes.append(nearest_city['name'])
    # print(nearest_city)
    route_distance += float(nearest_city['distance'])
    route_object = nearest_neighbor(cities_dictionary[nearest_city['name']],
        cities_dictionary, unchecked_cities_dictionary, routes, route_distance)
    return route_object

def nearest_insertion(city_a, cities_dictionary,
    unchecked_cities_dictionary=None , routes=None):
    """Nearest Insertion Algoritm."""
    # print(cities_dictionary)
    if unchecked_cities_dictionary is None:
        unchecked_cities_dictionary = cities_dictionary.copy()
        unchecked_cities_dictionary.pop(city_a['name'])
    if len(unchecked_cities_dictionary) < 1:
        total_distance = 0
        route_list = []
        for route in routes:
            route_list.append(route[0])
            # print(route[0]['name'], " | ", route[1]['name'], " | ", route[2])
            total_distance += route[2]
        return {'startingCity':route_list[0],'routes':route_list, 'route_distance': total_distance}
    nearest_city = None
    lowest_scored_route = None
    for next_city, next_data in unchecked_cities_dictionary.items():
        distance = distance_between_cities(city_a, next_data)
        if nearest_city is None:
            nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
        else:
            if distance < nearest_city['distance']:
                nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
    if nearest_city is None:
        # print(cities_dictionary)
        error = "Error in the program: no nearest_city"
        print(error)
        total_distance = 0
        route_list = []
        for route in routes:
            route_list.append(route[0])
            total_distance += route[2]
        return {'startingCity':route_list[0],'routes':route_list, 'route_distance':
            total_distance, 'error': error}
    unchecked_cities_dictionary.pop(nearest_city['object']['name'])
    if routes is None:
        routes = [[city_a, nearest_city['object'], nearest_city['distance']],
            [nearest_city['object'], city_a, nearest_city['distance']]]
    else:
        for index, route in enumerate(routes):
            distance_i_k = distance_between_cities(route[0], nearest_city['object'])
            distance_k_j = distance_between_cities(nearest_city['object'], route[1])
            score = distance_i_k + distance_k_j - route[2]
            if lowest_scored_route is None:
                lowest_scored_route = { 'index': index, 'city_i': route[0], 'city_k':
                    nearest_city['object'], 'city_j': route[1],
                        'city_i_to_city_k_distance': distance_i_k, 'city_k_to_city_j_distance':
                            distance_k_j, 'score': score}
            else:
                if score < lowest_scored_route['score']:
                    lowest_scored_route = { 'index': index,'city_i': route[0], 'city_k':
                        nearest_city['object'], 'city_j': route[1], 'city_i_to_city_k_distance':
                            distance_i_k, 'city_k_to_city_j_distance': distance_k_j, 'score': score}
        if lowest_scored_route is None:
            # print(cities_dictionary)
            error = "Error in the program: no lowest_scored_route"
            print(error)
            total_distance = 0
            route_list = []
            for route in routes:
                route_list.append(route[0])
                total_distance += route[2]
            return {'startingCity':route_list[0],'routes':route_list, 'route_distance':
                total_distance, 'error': error}
        # print(lowest_scored_route['city_i_to_city_k_distance'], " | ",
        #   lowest_scored_route["city_k_to_city_j_distance"])
        routes[lowest_scored_route['index']] = [lowest_scored_route['city_k'],
            lowest_scored_route['city_j'], lowest_scored_route['city_k_to_city_j_distance']]
        routes.insert(lowest_scored_route['index'], [lowest_scored_route['city_i'],
            lowest_scored_route['city_k'], lowest_scored_route['city_i_to_city_k_distance']])

    route_object = nearest_insertion(nearest_city['object'],
                     cities_dictionary, unchecked_cities_dictionary, routes)
    # print(nearest_city, " | ", route_object)
    return route_object


def cheapest_insertion(city_a, cities_dictionary,
    unchecked_cities_dictionary=None , routes=None):
    """Nearest Insertion Algoritm."""
    # print(cities_dictionary)
    if unchecked_cities_dictionary is None:
        unchecked_cities_dictionary = cities_dictionary.copy()
        unchecked_cities_dictionary.pop(city_a['name'])
    if len(unchecked_cities_dictionary) < 1:
        total_distance = 0
        route_list = []
        for route in routes:
            route_list.append(route[0])
            # print(route[0]['name'], " | ", route[1]['name'], " | ", route[2])
            total_distance += route[2]
        return {'startingCity':route_list[0],'routes':route_list, 'route_distance': total_distance}
    nearest_city = None
    lowest_scored_route = None
    if routes is None:
        for next_city, next_data in unchecked_cities_dictionary.items():
            distance = distance_between_cities(city_a, next_data)
            if nearest_city is None:
                nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
            else:
                if distance < nearest_city['distance']:
                    nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
        if nearest_city is None:
            # print(cities_dictionary)
            error = "Error in the program: no nearest_city"
            print(error)
            total_distance = 0
            route_list = []
            for route in routes:
                route_list.append(route[0])
                total_distance += route[2]
            return {'startingCity':route_list[0],'routes':route_list, 'route_distance':
                total_distance, 'error': error}
        unchecked_cities_dictionary.pop(nearest_city['object']['name'])
        routes = [[city_a, nearest_city['object'], nearest_city['distance']],
            [nearest_city['object'], city_a, nearest_city['distance']]]
    else:
        for index, route in enumerate(routes):
            for _, city_data in unchecked_cities_dictionary.items():
                distance_i_k = distance_between_cities(route[0], city_data)
                distance_k_j = distance_between_cities(city_data, route[1])
                score = distance_i_k + distance_k_j - route[2]
                if lowest_scored_route is None:
                    lowest_scored_route = { 'index': index, 'city_i': route[0], 'city_k':
                        city_data, 'city_j': route[1],
                            'city_i_to_city_k_distance': distance_i_k, 'city_k_to_city_j_distance':
                                distance_k_j, 'score': score}
                else:
                    if score < lowest_scored_route['score']:
                        lowest_scored_route = { 'index': index,'city_i': route[0], 'city_k':
                            city_data, 'city_j': route[1], 'city_i_to_city_k_distance':
                                distance_i_k, 'city_k_to_city_j_distance':
                                    distance_k_j, 'score': score}
        if lowest_scored_route is None:
            # print(cities_dictionary)
            error = "Error in the program: no lowest_scored_route"
            print(error)
            total_distance = 0
            route_list = []
            for route in routes:
                route_list.append(route[0])
                total_distance += route[2]
            return {'startingCity':route_list[0],'routes':route_list, 'route_distance':
                total_distance, 'error': error}
        # print(lowest_scored_route['city_i_to_city_k_distance'], " | ",
        #   lowest_scored_route["city_k_to_city_j_distance"])
        routes[lowest_scored_route['index']] = [lowest_scored_route['city_k'],
            lowest_scored_route['city_j'], lowest_scored_route['city_k_to_city_j_distance']]
        routes.insert(lowest_scored_route['index'], [lowest_scored_route['city_i'],
            lowest_scored_route['city_k'], lowest_scored_route['city_i_to_city_k_distance']])

    route_object = nearest_insertion(nearest_city['object'],
                     cities_dictionary, unchecked_cities_dictionary, routes)
    # print(nearest_city, " | ", route_object)
    return route_object



def process_algorithm(algorithm_function, cities_algorithm_dictionary):
    """Process to work through each Algoritm."""
    nearest_neighbor_route_dictionary = {}
    shortest_trip = None
    longest_trip = None
    total_distance = 0
    for city, data in cities_algorithm_dictionary.items():
        global_cities_dictionary = cities_algorithm_dictionary.copy()
        nearest_neighbor_route = algorithm_function(data, global_cities_dictionary)
        nearest_neighbor_route_dictionary[city] = nearest_neighbor_route
        total_distance += nearest_neighbor_route['route_distance']
        if shortest_trip is None:
            shortest_trip = nearest_neighbor_route
            longest_trip = nearest_neighbor_route
        else:
            if shortest_trip['route_distance'] > nearest_neighbor_route['route_distance']:
                shortest_trip = nearest_neighbor_route
            elif longest_trip['route_distance'] < nearest_neighbor_route['route_distance']:
                longest_trip = nearest_neighbor_route
    average_distance = total_distance / len(nearest_neighbor_route_dictionary)
    table_dictionary_entry = {}
    table_dictionary_entry['max'] = longest_trip
    table_dictionary_entry['min'] = shortest_trip
    table_dictionary_entry['avg'] = average_distance
    return table_dictionary_entry

cities = dictBuilder.read_csv(FILENAME)
tableDictionary = {}
algorithm_list = [{'name':'Nearest Neighbor', 'algorithm': nearest_neighbor},
        {'name':'Nearest Insertion', 'algorithm': nearest_insertion}, {'name':'Cheapest Insertion',
            'algorithm': cheapest_insertion}]
for algorithm in algorithm_list:
    tableDictionary[algorithm['name']] = process_algorithm(algorithm['algorithm'], cities)
    print(algorithm['name'])
    print(tableDictionary[algorithm['name']]['max']['route_distance'])
    print(tableDictionary[algorithm['name']]['min']['route_distance'])
    print(tableDictionary[algorithm['name']]['avg'])
# nearest_neighbor_route = nearest_neighbor(cities['Newark_NJ'], cities)
# print(nearest_neighbor_route)
# dist = distanceBetweenCities(cities['Chicago_IL'], cities['NewYork_NY'])
