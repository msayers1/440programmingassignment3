"""Module providing a driver for the Distance and algorithm comparisions."""
# Import math LibraryB
import math
import dict_builder
# Set some initial conditions.
FILENAME = "49Cities.csv"
RADIUS = 3958.8
DEG_TO_RAD = math.pi/180

def distance_between_cities(city_a, city_b):
    """Distance between two cites function."""
    # grabs the data from the two cities.
    lat_a = float(city_a['lat'])
    lat_b = float(city_b['lat'])
    long_a = float(city_a['long'])
    long_b = float(city_b['long'])
    # does the math to get the distance.
    return ((2 * RADIUS) * (math.asin(math.sqrt(.5 - (math.cos((lat_a - lat_b) * DEG_TO_RAD)/2)
        + math.cos(lat_b*DEG_TO_RAD) * math.cos(lat_a*DEG_TO_RAD) * (1-(math.cos((long_a - long_b)
        * DEG_TO_RAD))) /2))))

def nearest_neighbor(city_a, cities_dictionary,
    unchecked_cities_dictionary=None, routes=None, route_distance=0):
    """Nearest Neighbor Algoritm."""
    # print(cities_dictionary)
    # checks if the unchecked dictionary is intiated and if not initiates it with the full list.
    if unchecked_cities_dictionary is None:
        unchecked_cities_dictionary = cities_dictionary.copy()
    # Pops off the city we are looking at.
    unchecked_cities_dictionary.pop(city_a['name'])
    # (Base Case) if the unchecked list is empty then return and start closing the recursions.
    if len(unchecked_cities_dictionary) == 0:
        # print(city_a, " | ", cities_dictionary[routes[0]], " | ", routes [0])
        route_distance += distance_between_cities(city_a, cities_dictionary[routes[0]])
        return {'startingCity':routes[0],'routes':routes, 'route_distance': route_distance}
    # if routes is empty then put the first city in it.
    if routes is None:
        routes = [city_a['name']]
    nearest_city = None
    # Now we find the nearest city.
    for next_city, next_data in unchecked_cities_dictionary.items():
        # This is a redundant check to make sure I haven't messed up somewhere.
        if next_city != city_a['name']:
            # takes the distance between the city we are checking and the city we are
            # keeping the same.
            distance = distance_between_cities(city_a, next_data)
            # If no nearest city is set, then set it.
            if nearest_city is None:
                nearest_city = {'name':next_city, 'distance':distance}
            else:
                if distance < nearest_city['distance']:
                    nearest_city = {'name':next_city, 'distance':distance}
    # Some problem arose.
    if nearest_city is None:
        # print(unchecked_cities_dictionary)
        print("Error in the program: no nearest_city")
        return {'startingCity':routes[0],'routes ':routes,
            'route_distance': route_distance, 'error': "Did not finish"}
    routes.append(nearest_city['name'])
    # print(nearest_city)
    route_distance += float(nearest_city['distance'])
    # Call the function to go recursive until the base case.
    route_object = nearest_neighbor(cities_dictionary[nearest_city['name']],
        cities_dictionary, unchecked_cities_dictionary, routes, route_distance)
    return route_object

def nearest_insertion(city_a, cities_dictionary,
    unchecked_cities_dictionary=None , routes=None):
    """Nearest Insertion Algoritm."""
    # print(cities_dictionary)
    # Checks if the unchecked dictionary is set and if not sets it
    if unchecked_cities_dictionary is None:
        unchecked_cities_dictionary = cities_dictionary.copy()
        # We pop the city within the first initation because we pop the city later on.
        unchecked_cities_dictionary.pop(city_a['name'])
    # (Base Case) this is checking if the unchecked city is empty,
    # if so build the route and start returning.
    if len(unchecked_cities_dictionary) < 1:
        total_distance = 0
        route_list = []
        # Loop through the routes to build in the format I use for nearest neighbor.
        for route in routes:
            route_list.append(route[0]['name'])
            # print(route[0]['name'], " | ", route[1]['name'], " | ", route[2])
            total_distance += route[2]
        return {'startingCity':route_list[0],'routes':route_list, 'route_distance': total_distance}
    nearest_city = None
    lowest_scored_route = None
    # Now we find the nearest city.
    for next_city, next_data in unchecked_cities_dictionary.items():
        # takes the distance between the city we are checking and the city we are
        # keeping the same.
        distance = distance_between_cities(city_a, next_data)
        # If no nearest city is set, then set it.
        if nearest_city is None:
            nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
        else:
            if distance < nearest_city['distance']:
                nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
    # Some problem arose.
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
    # Instead of waiting for the recursive call of the function, I pop the city here.
    unchecked_cities_dictionary.pop(nearest_city['object']['name'])
    # If no routes have been set, set the first one.
    if routes is None:
        routes = [[city_a, nearest_city['object'], nearest_city['distance']],
            [nearest_city['object'], city_a, nearest_city['distance']]]
    # Else figure out the next segment to insert.
    else:
        # Loop thourgh all the routes and find the one that creates the lowest
        # "distance of i to k + distance of k to j - distance of i to j"
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
        # Some problem arose.
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
    # Call the function to go recursive until the base case.
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
    # (Base Case) this is checking if the unchecked city is empty,
    # if so build the route and start returning.
    if len(unchecked_cities_dictionary) < 1:
        total_distance = 0
        route_list = []
        for route in routes:
            route_list.append(route[0]['name'])
            # print(route[0]['name'], " | ", route[1]['name'], " | ", route[2])
            total_distance += route[2]
        return {'startingCity':route_list[0],'routes':route_list, 'route_distance': total_distance}
    nearest_city = None
    lowest_scored_route = None
    # Now we find the nearest city, since you have only one city.
    if routes is None:
        for next_city, next_data in unchecked_cities_dictionary.items():
            # takes the distance between the city we are checking and the city we are
            # keeping the same.
            distance = distance_between_cities(city_a, next_data)
            if nearest_city is None:
                nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
            else:
                if distance < nearest_city['distance']:
                    nearest_city = {'name': next_city, 'object':next_data, 'distance':distance}
        # Some problem arose.
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
        # Loop through all the routes already added.
        for index, route in enumerate(routes):
            # Loop thourgh all the cities and find the one that creates the lowest
            # "distance of i to k + distance of k to j - distance of i to j"
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
        # Some problem arose.
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
    # Call the function to go recursive until the base case.
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
    # Iterates over the dictionary
    for city, data in cities_algorithm_dictionary.items():
        global_cities_dictionary = cities_algorithm_dictionary.copy()
        nearest_neighbor_route = algorithm_function(data, global_cities_dictionary)
        nearest_neighbor_route_dictionary[city] = nearest_neighbor_route
        total_distance += nearest_neighbor_route['route_distance']
        # Checks to see if is not defined and sets it.
        if shortest_trip is None:
            shortest_trip = nearest_neighbor_route
            longest_trip = nearest_neighbor_route
        # It was set so now it will do the checks.
        else:
            if shortest_trip['route_distance'] > nearest_neighbor_route['route_distance']:
                shortest_trip = nearest_neighbor_route
            elif longest_trip['route_distance'] < nearest_neighbor_route['route_distance']:
                longest_trip = nearest_neighbor_route
    average_distance = total_distance / len(nearest_neighbor_route_dictionary)
    table_dictionary_entry = {}
    # Records the data into the dictionary.
    table_dictionary_entry['max'] = longest_trip
    table_dictionary_entry['min'] = shortest_trip
    table_dictionary_entry['avg'] = average_distance
    return table_dictionary_entry

def main():
    """Main function."""
    cities = dict_builder.read_csv(FILENAME)
    table_dictionary = {}
    output_string = ''
    table_dictionary['shortestTour'] = {}
    table_dictionary['longestTour'] = {}
    table_dictionary['averageOfAllTours'] = {}
    algorithm_list = [{'name':'Nearest Neighbor', 'algorithm': nearest_neighbor},
            {'name':'Nearest Insertion', 'algorithm': nearest_insertion},
                {'name':'Cheapest Insertion', 'algorithm': cheapest_insertion}]
    for algorithm in algorithm_list:
        table_dictionary[algorithm['name']] = process_algorithm(algorithm['algorithm'], cities)
        min_route_object = table_dictionary[algorithm['name']]['min']
        table_dictionary['shortestTour'][algorithm['name']] = min_route_object
        max_route_object = table_dictionary[algorithm['name']]['max']
        table_dictionary['longestTour'][algorithm['name']] = max_route_object
        avg_route_object = table_dictionary[algorithm['name']]['avg']
        table_dictionary['averageOfAllTours'][algorithm['name']] = avg_route_object
        # print(algorithm['name'])
        # print(table_dictionary[algorithm['name']]['max']['route_distance'])
        # print(table_dictionary[algorithm['name']]['min']['route_distance'])
        # print(table_dictionary[algorithm['name']]['avg'])
    print("\t\tNearest Neigbhor\tNearest Insertion\tCheapest Insertion\n")
    output_string += "Shortest Tour:\t"
    for algorithm in table_dictionary['shortestTour']:
        output_string += str(table_dictionary['shortestTour'][algorithm]['route_distance']) + "\t"
    print(output_string, '\n')
    output_string = ''
    output_string += "Average Tour:\t"
    for algorithm in table_dictionary['averageOfAllTours']:
        output_string += str(table_dictionary['averageOfAllTours'][algorithm]) + "\t"
    print(output_string, "\n")
    output_string = ''
    output_string += "Longest Tour:\t"
    for algorithm in table_dictionary['longestTour']:
        output_string += str(table_dictionary['longestTour'][algorithm]['route_distance']) + "\t"
    print(output_string, "\n")
    output_string = ''
    output_string += "Shortest Tour's Tour route:\n\n"
    for algorithm in algorithm_list:
        output_string += algorithm['name'] + '\n'
        for city_o in table_dictionary[algorithm['name']]['min']['routes']:
            output_string += " " + city_o + " "
        output_string += '\n\n'
    print("\n", output_string)
    # nearest_neighbor_route = nearest_neighbor(cities['Newark_NJ'], cities)
    # print(nearest_neighbor_route)
    # dist = distanceBetweenCities(cities['Chicago_IL'], cities['NewYork_NY'])
if __name__ == "__main__":
    main()
