# Extract information per map from 
# Karrow's Index to Place and Date
# in Sixteenth Century Mapmakers and Their Maps

# Code by Erin Watson
# May 13, 2024

import re 
import pandas as pd

# Open up the cleaned file
with open('../cleaned-ocr-text/index_to_place_and_date.txt') as f:
    index = f.read()

"""
Strategy for parsing
1. Split the string based on the countries 
2. Grab the country, remove it from the rest of the string
3. Split by cities 
4. For each city, grab the name and remove it from the rest of the string
5. For each city, split into years. Each year ends with a semicolon if there is not another
6. For each year, strip whitespace (since entries are separated by commas) and split on commas
7. For each entry, grab the mapmaker (first part), map/book (second part)
8. Some entries have many maps or books in a range indicated by a hyphen, expand these 
"""

# 1. Split the string based on the countries
by_country = index.split("\n\n")

# Make a dictionary to store the data
# (eventually we will convert this to a pandas dataframe)
# columns are: mapmaker, map/book ID, country, city, date
index_data = {"mapmaker_id": [], "map_or_book_id": [], "country": [], "city": [], "date": []}

for country_data in by_country:
    # 2. Grab the country, remove it from the rest of the string
    country_name = country_data.split("\n")[0]
    country_data = country_data.replace(country_name, "").strip()

    # 3. Split by cities
    by_city = re.split("—|一", country_data)

    # 4. For each city, grab the name and remove it from the rest of the string
    for city_data in by_city[1:]: # skip the first element, which is empty
        # grab the city name
        city_name = re.split(":", city_data)[0]
        city_name = city_name.strip() # remove leading/trailing whitespace

        # remove the city name from the data
        city_data = city_data.replace(city_name, "").strip()

        # remove the leading colon and space left over from the city name
        if city_data[0:2] == ": ":
            city_data = city_data[2:]
        if city_data[0:1] == ":":
            city_data = city_data[1:]

        # 5. For each city, split into years. Each year ends with a semicolon if there is not another
        by_date = city_data.split(";") 

        # 6. For each year, strip whitespace (since entries are separated by commas) and split on commas
        for date_data in by_date:
            # grab the date
            date = re.split(",", date_data)[0]
            date = date.strip()

            # remove the date from the data
            date_data = date_data.replace(date, "").strip()

            # remove the leading comma and space left over from the date
            if date_data[0:2] == ", ":
                date_data = date_data[2:]
            if date_data[0:1] == ",":
                date_data = date_data[1:]

            # split the data by entry 
            by_entry = date_data.split(",")

            # 7. For each entry, grab the mapmaker (first part), map/book, and then any notes (like editions or alternate years?)
            for entry_data in by_entry:
                entry_data = entry_data.strip()
                # remove newline characters
                entry_data = entry_data.replace("\n", "")
                print(entry_data)

                # Separate the mapmaker and the map/book ID
                mapmaker_id = entry_data.split("/")[0]

                try:
                    object_id = entry_data.split("/")[1]
                except:
                    print("Error: object id in incorrect format")
                    print(entry_data)
                    print()
                    continue

                # Maps are numbered, Books have letters
                capital_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL', 'MM', 'NN', 'OO', 'PP', 'QQ', 'RR', 'SS', 'TT', 'UU', 'VV', 'WW', 'XX', 'YY', 'ZZ']

                # 8. Some entries have many maps or books in a range indicated by a hyphen, expand these
                if "-" in object_id:
                    # grab the range of IDs
                    start_id = object_id.split("-")[0]
                    end_id = object_id.split("-")[1]

                    # check if both are first editions or later editions (which have a period)
                    if "." in start_id and "." in end_id:
                        # both are later editions
                        # check if both are the same edition
                        if start_id.split(".")[1] == end_id.split(".")[1]:
                            # they are the same edition, 
                            # assume that the range means all maps / books in between 
                            # had the same edition as well.
                            start_id_general = start_id.split(".")[0]
                            end_id_general = end_id.split(".")[0]
                            edition = start_id.split(".")[1]

                            # If it's a book, there are letters for the IDs
                            if start_id_general in capital_alphabet and end_id_general in capital_alphabet:
                                book_range_index = (capital_alphabet.index(start_id_general), capital_alphabet.index(end_id_general))

                                if book_range_index[0] > book_range_index[1]:
                                    print("Error: book range is reversed")
                                    print(entry_data)
                                    print()

                                else:
                                    for i in range(book_range_index[0], book_range_index[1] + 1):
                                        index_data["mapmaker_id"].append(mapmaker_id)
                                        index_data["map_or_book_id"].append(f"{capital_alphabet[i]}.{edition}")
                                        index_data["country"].append(country_name)
                                        index_data["city"].append(city_name)
                                        index_data["date"].append(date)
                            
                            elif (WE HAVE MAPS NOT BOOKS):
                                    

                    elif "." not in start_id and "." not in end_id:
                        # neither are later editions
                        pass

                    else:
                        print("Error: range has mixed editions")
                        print(entry_data)
                        print()
                        continue

                    # end range case
                                    

                else: # no hyphen, assume no range
                    index_data["mapmaker_id"].append(mapmaker_id)
                    index_data["map_or_book_id"].append(object_id)
                    index_data["country"].append(country_name)
                    index_data["city"].append(city_name)
                    index_data["date"].append(date)


                                



