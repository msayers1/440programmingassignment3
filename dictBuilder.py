import csv

def read_csv(file_name):
    data = {}
    with open(file_name, 'r',encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # print(row) 
            data[row['city_state']] = { 'name':row['city_state'], 'lat': row['lat'], 'long': row['long']}
    return data
if __name__ == "__main__":
    FILENAME = "49Cities.csv"
    cities = read_csv(FILENAME)
    print(cities)
    # for city, data in cities.items():
    #     print(city, " | ", data['lat'], " | ", data['long'] )
