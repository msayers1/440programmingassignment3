"""
Args:
-m or --mode: Score or Game.
-g or --game_name: Path to the cards.
-p or --players: Number of Players 

Returns:
Nothing, prints out people's score and error messages for card.txt without a matching edge.txt
"""
import sys
import dict_builder
import driver_all_cities
algorithm_list = [{'name':'Nearest Neighbor', 'algorithm': driver_all_cities.nearest_neighbor},
        {'name':'Nearest Insertion', 'algorithm': driver_all_cities.nearest_insertion},
            {'name':'Cheapest Insertion', 'algorithm': driver_all_cities.cheapest_insertion}]
FILENAME = "49Cities.csv"
cities_algorithm_dictionary_driver_local = dict_builder.read_csv(FILENAME)
tableDictionary = {}
output_string = ""

def process_algorithm(starting_city, algorithm_function, cities_algorithm_dictionary_local):
    """Process to work through each Algoritm."""
    table_dictionary_entry = algorithm_function(starting_city, cities_algorithm_dictionary_local)
    return table_dictionary_entry
if __name__ == "__main__":
    entry = None
    if len(sys.argv) > 1:
        starting_city = sys.argv[1]
        for algorithm in algorithm_list:
            entry = process_algorithm(cities_algorithm_dictionary_driver_local[starting_city],
                algorithm['algorithm'], cities_algorithm_dictionary_driver_local)
            tableDictionary[algorithm['name']] = entry
            print(algorithm['name'])
            print('\t', tableDictionary[algorithm['name']]['route_distance'])
            output_string += '\t'
            for city_o in tableDictionary[algorithm['name']]['routes']:
                output_string += " " + city_o + " "
            print(output_string, "\n")
            output_string = ''
    else:
        driver_all_cities.main()
    #     args = sys.argv[1]
    # print(args)
